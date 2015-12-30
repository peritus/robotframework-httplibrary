

def run_cli(args):
    # abstracts away this change
    # https://code.google.com/p/robotframework/source/detail?r=ebc6fbb542e6
    # so we can test this lib against RF 2.6 and 2.7 w/o much config overhead

    import robot
    try:
        robot.run_cli(args)
    except Exception as e:
        print(e)
        import robot.runner
        robot.run_from_cli(args, robot.runner.__doc__)
