def summary_var(grads):
    for grad, var in grads:
        if grad is not None:
            tf.summary.histogram(var.op.name + '/gradients', grad)
        for var in tf.trainable_variables():
            tf.summary.histogram(var.op.name, var)


def train_step(tower_grads, optimizer, summary_callback, name='train_step', clipv=None):
    """
    Inputs:
        tower_grads: *list or tuple* of grads
        optimizer: optimizer
    """
    with tf.name_scope(name), tf.device('/cpu:0'):
        average_grads = []
        for grad_and_vars in zip(*tower_grads):
            # Note that each grad_and_vars looks like the following:
            #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
            grads = []
            for g, _ in grad_and_vars:

                # Add 0 dimension to the gradients to represent the tower.
                expanded_g = tf.expand_dims(g, 0)

                # Append on a 'tower' dimension which we will average over
                # below.
                grads.append(expanded_g)
            # Average over the 'tower' dimension.
            grad = tf.concat(axis=0, values=grads)
            grad = tf.reduce_mean(grad, 0)
            if clipv is not None:
                grad = tf.clip_by_value(grad, -clipv, clipv)
            # Keep in mind that the Variables are redundant because they are shared
            # across towers. So .. we will just return the first tower's pointer to
            # the Variable.
            v = grad_and_vars[0][1]
            grad_and_var = (grad, v)
            average_grads.append(grad_and_var)
        train_op = optimizer.apply_gradients(
            average_grads, global_step=self.gs)

        if summary_callback is not None:
            summary_callback(average_grads)
    return train_op
