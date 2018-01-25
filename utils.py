import json

def is_json(myjson):
  try:
    x = json.loads(myjson)
  except Exception:
    return False
  return True

def normalise(action):
    if  type(action) == list:
        final_action = []
        for x in action:
            final_action.append(normalise_action(x))
    else:
        final_action = normalise_action(action)
    return final_action

def normalise_action(action):
    positive_action = action + 1
    final_action = positive_action / 2
    return final_action

def boolean_flag(parser, name, default=False, help=None):
    """Add a boolean flag to argparse parser.

    Parameters
    ----------
    parser: argparse.Parser
        parser to add the flag to
    name: str
        --<name> will enable the flag, while --no-<name> will disable it
    default: bool or None
        default value of the flag
    help: str
        help string for the flag
    """
    dest = name.replace('-', '_')
    parser.add_argument("--" + name, action="store_true", default=default, dest=dest, help=help)
    parser.add_argument("--no-" + name, action="store_false", dest=dest)