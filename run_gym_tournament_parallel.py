import os
import argparse
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import time
import itertools
from multiprocessing import Pool
import make_env
import warnings
warnings.filterwarnings("ignore")

def run_single_step(project_part, T, headtohead, return_fig=False):
    """
    Run a single round of the round-robin tournament as a head-to-head match up.
    """

    # Each step will be a single head-to-head competition
    assert len(headtohead) == 2

    if project_part == 1:
        env, agents = make_env.make_env_agents(agentnames = headtohead, project_part = project_part)
    else:
        env, agents = make_env.make_env_agents(agentnames = headtohead, project_part = project_part,
                                               first_file = 'data/datafile1.csv', second_file='data/datafile2.csv')
    
    # Run head-to-head
    env.reset()
    customer_covariates, sale, profits = env.get_current_state_customer_to_send_agents()
    last_customer_covariates = customer_covariates
    cumulativetimes = [0 for _ in agents]
    
    if return_fig:
        fig, ax = plt.subplots(figsize=(20, 10))
    else:
        fig = []

    for t in range(0, T):
        
        actions = []
        for enoutside, agent in enumerate(agents):
            ts = time.time()
            
            action = agent.action((customer_covariates, sale, profits))
            # Have to give 1 price for each item. There is 1 item in part 1, 2 items in part 2
            assert len(action) == project_part
            
            curtime = time.time()
            cumulativetimes[enoutside] += curtime - ts
            actions.append(action)
            
        customer_covariates, sale, profits = env.step(actions)
        if return_fig:
            newplot = env.render(True)

        last_customer_covariates = customer_covariates
    if return_fig:
        fig = plt.gcf()
        plt.close()

    return fig, env.cumulative_buyer_utility, headtohead, profits, list(map(lambda x: x/T, cumulativetimes))



def main(project_part, T):
    """
    Simulate a round-robin dynamic pricing under competition tournament

    project_part : int
        TODO Change this for whether you're coding for part 1 or part 2!
    T : int
        Number of rounds (time-steps)
    agentnames : list(str)
        Replace the agentnames to match whatever agentfiles you create. You can use the same agentnames for both agents
    """
    
    all_agents = list(
        map(lambda x: x.replace('.py', ''), filter(lambda x: ('.py' in x) and ('__init__' not in x), os.listdir('agents/')))
    )

    # using multiprocessing
    start_time = time.perf_counter()
    with Pool() as pool:
        pooled_results = pool.starmap(run_single_step, [(project_part, T, pair) for pair in list(itertools.combinations(all_agents, 2))])
    finish_time = time.perf_counter()

    # clean up competition results and save
    results = {
        'fig': [x[0] for x in pooled_results],
        'buyer_utility': [x[1] for x in pooled_results],
        'agent0': [x[2][0] for x in pooled_results],
        'profit0': [x[3][0] for x in pooled_results],
        'avg_runtime0': [x[4][0] for x in pooled_results],
        'agent1': [x[2][1] for x in pooled_results],
        'profit1': [x[3][1] for x in pooled_results],
        'avg_runtime1': [x[4][1] for x in pooled_results]
    }
    df = pd.DataFrame(results).sort_values(by='buyer_utility', ascending=False).reset_index(drop=True)
    pickle.dump(df, open('data/tournament_results.pickle', 'wb'))
        
    # Publish rankings
    ranking_profit = pd.concat([
        df[['agent0', 'profit0']].rename(columns={'agent0': 'agent', 'profit0': 'profit'}),
        df[['agent1', 'profit1']].rename(columns={'agent1': 'agent', 'profit1': 'profit'})
    ]).groupby('agent').profit.mean().sort_values(ascending=False)
    ranking_runtime = pd.concat([
        df[['agent0', 'avg_runtime0']].rename(
            columns={'agent0': 'agent', "avg_runtime0": "avg_runtime"}),
        df[['agent1', 'avg_runtime1']].rename(
            columns={'agent1': 'agent', "avg_runtime1": "avg_runtime"})
    ]).groupby('agent').avg_runtime.mean() * 1000
    ranking = pd.merge(ranking_profit, ranking_runtime, on="agent").reset_index()

    
    print("---")
    print('Tournament Ranking:\n\n', ranking)
    print("\nProgram finished in {} seconds - using multiprocessing".format(finish_time-start_time))
    print("---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs head to head competitions in parallel to simulate tournament results",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter          
    )
    parser.add_argument("-p", "--part", default=2, type=int)
    parser.add_argument("-T", "--timesteps", default=500, type=int)
    args = parser.parse_args()

    main(args.part, args.timesteps)