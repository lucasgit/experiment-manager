'''
Created on Apr 24, 2016

@author: Lucas Lehnert (lucas.lehnert@mail.mcgill.ca)
'''
import json

def main():
    import argparse
    parser = argparse.ArgumentParser( description='Test Experiment', \
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument( '-r', '--resultFile', type=str, default='../experiment/test.json', help='Result file path.' )
    parser.add_argument( '-e', '--episodes', type=int, default=1, help='Number of episodes to run.' )
    parser.add_argument( '-i', '--iterations', type=int, default=1, help='Number of iterations to run.' )
    parser.add_argument( '-a', '--alpha', type=float, default=1, help='Learning rate to run.' )

    args = parser.parse_args()


    resFile = args.resultFile
    episodes = args.episodes
    iterations = args.iterations
    alpha = args.alpha

    dict = {'episodes' : episodes, 'iterations' : iterations, 'alpha' : alpha}
    with open( resFile, 'wb' ) as fp:
        json.dump( dict, fp )

    print 'Done with experimenting.'

if __name__ == '__main__':
    main()
    pass
