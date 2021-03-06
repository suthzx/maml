"""
Test models
"""
from unittest import TestCase, main

import numpy as np

from maml.model import DeepSets
from maml.describer import SiteElementProperty


class TestDeepSets(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.x = np.array([[0, 1, 0, 1, 0, 1]], dtype=np.int32).reshape((1, -1))
        cls.x_vec = np.random.normal(size=(1, 6, 20))
        cls.indices = np.array([[0, 0, 0, 1, 1, 1]], dtype=np.int32).reshape((1, -1))
        cls.y = np.array([[0.1, 0.2]]).reshape((1, 2, 1))
        cls.model1 = DeepSets(
            describer=None,
            is_embedding=True, n_neurons=(4, 4), n_neurons_final=(4, 4))
        cls.model2 = DeepSets(
            input_dim=20,
            is_embedding=False,
            n_neurons=(4, 4), n_neurons_final=(4, 4))
        cls.model3 = DeepSets(
            input_dim=20,
            is_embedding=False,
            symmetry_func='set2set',
            n_neurons=(4, 4), n_neurons_final=(4, 4),
            T=2,
            n_hidden=10)

    def test_predict(self):
        res = self.model1.model.predict([self.x, self.indices])
        self.assertTrue(res.shape == (1, 2, 1))
        res2 = self.model2.model.predict([self.x_vec, self.indices])
        self.assertTrue(res2.shape == (1, 2, 1))
        res3 = self.model3.model.predict([self.x_vec, self.indices])
        self.assertTrue(res3.shape == (1, 2, 1))

    def test_train(self):
        s = ['H', 'H2O', 'O2', 'OH', 'H3O']
        targets = [0., 1./3, 1, 0.5, 1./4]
        model = DeepSets(describer=SiteElementProperty(),
                         is_embedding=True,
                         symmetry_func='mean',
                         n_neurons=(8, 8),
                         n_neurons_final=(4, 4),
                         n_targets=1)
        model.train(s, targets, epochs=1)
        self.assertTrue(model.predict_objs(['H2']).shape == (1, 1))


if __name__ == "__main__":
    main()
