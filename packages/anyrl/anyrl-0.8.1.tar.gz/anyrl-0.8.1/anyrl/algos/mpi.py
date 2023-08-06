"""
Utilities for distributed training with MPI.
"""

from mpi4py import MPI
import numpy as np
import tensorflow as tf

# pylint: disable=E1101

# pylint: disable=R0903
class MPIOptimizer:
    """
    Wraps a TensorFlow optimizer to use MPI allreduce.
    """
    def __init__(self, optimizer, loss, var_list=None):
        self.grads = optimizer.compute_gradients(loss, var_list=var_list)

        # TODO: make sure gradients will be ordered
        # deterministically.

        self.placeholders = []
        apply_in = []
        for grad, var in self.grads:
            placeholder = tf.placeholder(dtype=grad.dtype, shape=grad.shape)
            self.placeholders.append(placeholder)
            apply_in.append((placeholder, var))
        self.apply = optimizer.apply_gradients(apply_in)

    def minimize(self, sess, feed_dict=None, terms=None):
        """
        Compute the gradients, aggregate them, and apply
        them using the wrapped optimizer.

        Arguments:
          sess: the TensorFlow session.
          feed_dict: the TensorFlow feed_dict for the
            objective.
          terms: a list of scalar Tensors to run at the
             same time as the gradient computation.

        Returns:
          A tuple containing the mean values for each
          entry in terms.
        """
        if not feed_dict:
            feed_dict = {}
        if not terms:
            terms = []
        outs = sess.run(terms + [x[0] for x in self.grads],
                        feed_dict=feed_dict)
        grad_outs = outs[len(terms):]
        term_outs = outs[:len(terms)]

        extra_feed = feed_dict.copy()
        for grad_out, placeholder in zip(grad_outs, self.placeholders):
            mean_grad = np.zeros(grad_out.shape, dtype='float32')
            send_grad = np.array(grad_out, dtype='float32')
            MPI.COMM_WORLD.Allreduce(send_grad, mean_grad, op=MPI.SUM)
            mean_grad /= MPI.COMM_WORLD.Get_size()
            extra_feed[placeholder] = mean_grad
        sess.run(self.apply, feed_dict=extra_feed)

        result = []
        for term in term_outs:
            total = MPI.COMM_WORLD.allreduce(term, op=MPI.SUM)
            result.append(total / MPI.COMM_WORLD.Get_size())
        return tuple(result)

# pylint: disable=R0913
def mpi_ppo(ppo, optimizer, rollouts, batch_size=None, num_iter=12, log_fn=None,
            extra_feed_dict=None):
    """
    Run the PPO inner loop with an MPI optimizer.

    If log_fn is set, logging is done on rank 0.
    """
    batch_idx = 0
    batches = ppo.model.batches(rollouts, batch_size=batch_size)
    advantages = ppo.adv_est.advantages(rollouts)
    targets = ppo.adv_est.targets(rollouts)
    for batch in batches:
        feed_dict = ppo.feed_dict(rollouts, batch,
                                  advantages=advantages,
                                  targets=targets)
        if extra_feed_dict:
            feed_dict.update(extra_feed_dict)
        terms = optimizer.minimize(ppo.model.session,
                                   feed_dict=feed_dict,
                                   terms=[ppo.actor_loss, ppo.critic_loss, ppo.entropy,
                                          ppo.num_clipped])
        if log_fn and MPI.COMM_WORLD.Get_rank() == 0:
            log_fn('batch %d: actor=%f critic=%f entropy=%f clipped=%d' %
                   (batch_idx, terms[0], terms[1], terms[2], terms[3]))
        batch_idx += 1
        if batch_idx == num_iter:
            break
