import random
import scipy.sparse as sp


def generate_dummy_data(num_users=15000, num_items=30000, interaction_density=.00045, pos_int_ratio=.5):

    n_user_features = int(num_users * 1.2)
    n_user_tags = num_users * 3
    n_item_features = int(num_items * 1.2)
    n_item_tags = num_items * 3
    n_interactions = (num_users * num_items) * interaction_density

    user_features = sp.lil_matrix((num_users, n_user_features))
    for i in range(num_users):
        user_features[i, i] = 1

    for i in range(n_user_tags):
        user_features[random.randrange(num_users), random.randrange(num_users, n_user_features)] = 1

    item_features = sp.lil_matrix((num_items, n_item_features))
    for i in range(num_items):
        item_features[i, i] = 1

    for i in range(n_item_tags):
        item_features[random.randrange(num_items), random.randrange(num_items, n_item_features)] = 1

    interactions = sp.lil_matrix((num_users, num_items))
    for i in range(int(n_interactions * pos_int_ratio)):
        interactions[random.randrange(num_users), random.randrange(num_items)] = 1

    for i in range(int(n_interactions * (1 - pos_int_ratio))):
        interactions[random.randrange(num_users), random.randrange(num_items)] = -1

    return interactions, user_features, item_features
