import os
import shutil
import unittest
from classes.utilitaires_01 import Utilitaires01


class TestUtilitaires01(unittest.TestCase):

    # =========================================================================

    # Test for directory_exists method
    def test_directory_exists(self):
        self.assertFalse(Utilitaires01.directory_exists('non_existent_path'))
        os.makedirs('test_dir')
        self.assertTrue(Utilitaires01.directory_exists('test_dir'))
        shutil.rmtree('test_dir')

    # =========================================================================

    # Test for create_folder method
    def test_create_folder(self):
        path = 'new_test_folder'
        if os.path.exists(path):
            shutil.rmtree(path)

        Utilitaires01.create_folder(path)
        self.assertTrue(os.path.isdir(path))

        # Test for existing folder
        with self.assertRaises(FileExistsError):
            Utilitaires01.create_folder(path)

        shutil.rmtree(path)

    # =========================================================================

    # Test for is_folder_empty method
    def test_is_folder_empty(self):
        path = 'empty_test_folder'
        os.makedirs(path)
        self.assertTrue(Utilitaires01.is_folder_empty(path))

        # Create a file in the folder, making it non-empty
        with open(os.path.join(path, 'file.txt'), 'w') as f:
            f.write('content')
        self.assertFalse(Utilitaires01.is_folder_empty(path))

        # Test for non-existent folder
        shutil.rmtree(path)
        self.assertRaises(FileNotFoundError,
                          Utilitaires01.is_folder_empty,
                          path)


if __name__ == '__main__':
    unittest.main()
