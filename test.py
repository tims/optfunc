import unittest
import optfunc

class TestOptFunc(unittest.TestCase):
    def test_three_positional_args(self):
        
        has_run = [False]
        def func(one, two, three):
            has_run[0] = True
        
        # Should only have the -h help option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 1)
        self.assertEqual(str(parser.option_list[0]), '-h/--help')
        
        # Should have three required args
        self.assertEqual(required_args, ['one', 'two', 'three'])
        
        # Running it with the wrong number of arguments should cause an error
        for argv in (
            ['one'],
            ['one', 'two'],
            ['one', 'two', 'three', 'four'],
        ):
            self.assertRaises(TypeError, optfunc.run, func, argv)
            self.assertEqual(has_run[0], False)
        
        # Running it with the right number of arguments should be fine
        optfunc.run(func, ['one', 'two', 'three'])
        self.assertEqual(has_run[0], True)
    
    def test_one_arg_one_option(self):
        
        has_run = [False]
        def func(one, two=optfunc.Var('-o', '--option')):
            has_run[0] = (one, two)
        
        # Should have -o option as well as -h option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 2)
        strs = [str(o) for o in parser.option_list]
        self.assert_('-h/--help' in strs)
        self.assert_('-o/--option' in strs)
        
        # Should have one required arg
        self.assertEqual(required_args, ['one'])
        
        # Should execute
        self.assert_(not has_run[0])
        optfunc.run(func, ['the-required', '-o', 'the-option'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('the-required', 'the-option'))
        
        # Option should be optional
        has_run[0] = False
        optfunc.run(func, ['required2'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('required2', None))

if __name__ == '__main__':
    unittest.main()