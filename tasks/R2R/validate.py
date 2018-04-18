import argparse
import utils
import train
from follower import Seq2SeqAgent

def validate_entry_point(args):
    agent, train_env, val_envs = train.train_setup(args)
    agent.load(args.model_prefix)

    for env_name, (env, evaluator) in val_envs.items():
        agent.env = env
        results = agent.test(use_dropout=False, feedback='argmax', beam_size=args.beam_size)
        score_summary, _ = evaluator.score_results(results)

        # TODO: testing code, remove
        # score_summary_direct, _ = evaluator.score_results(agent.results)
        # assert score_summary == score_summary_direct

        for metric,val in score_summary.items():
            print("{} {}\t{}".format(env_name, metric, val))

def make_arg_parser():
    parser = train.make_arg_parser()
    parser.add_argument("model_prefix")
    parser.add_argument("--beam_size", type=int, default=1)
    return parser

if __name__ == "__main__":
    utils.run(make_arg_parser(), validate_entry_point)