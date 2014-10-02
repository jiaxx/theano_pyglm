import numpy as np

import theano.tensor as T
from pyglm.components.component import Component


def create_bias_component(model, glm, latent):
    type = model['bias']['type'].lower()
    if type == 'constant':
        bias = TheanoConstantBias(model)
    else:
        raise Exception("Unrecognized bias model: %s" % type)
    return bias

class _ConstantBiasBase(Component):

    @property
    def I_bias(self):
        raise NotImplementedError()

    @property
    def log_p(self):
        raise NotImplementedError()

class TheanoConstantBias(_ConstantBiasBase):
    """
    """
    def __init__(self, model):
        """ Initialize a simple scalara bias. This is only in a class
            for consistency with the other model components
        """

        prms = model['bias']
        self.mu_bias = prms['mu']
        self.sig_bias = prms['sigma']

        # Define a bias to the membrane potential
        # TODO: Figure out if we can get around the vector requirement for grads
        self.bias = T.dvector('bias')
        self._I_bias = self.bias[0]
        self._log_p = -0.5/self.sig_bias**2 * (self.bias[0] - self.mu_bias)**2

    @property
    def I_bias(self):
        return self._I_bias

    @property
    def log_p(self):
        return self._log_p

#         self.f_I_bias = theano.function(self.bias,self.bias)

    def get_variables(self):
        """ Get the theano variables associated with this model.
        """
        return {str(self.bias) : self.bias}

    def set_hyperparameters(self, model):
        """ Set the hyperparameters of the model
        """
        self.mu_bias = model['mu']
        self.sig_bias = model['sigma']

    def get_state(self):
        return {'bias': self.bias}
    
    def sample(self, acc):
        """
        return a sample of the variables
                """
        b = self.mu_bias + self.sig_bias * np.random.randn(1,)
        return {str(self.bias) : b}
