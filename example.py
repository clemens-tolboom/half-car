import argparse
from halfcar import Car, PlotSim, Road


def simulate(car, time_step=0.0002, interval=1):
    """
    TODO
    """

    elapsed_time = 0
    iteration = 0
    while True:
        ######################################################################
        ######################################################################
        ########### SET THE DESIRED SIMULATION PARAMETERS HERE ###############
        if 0 <= elapsed_time < 8:
            car.set_accel(4.4)
        elif 8 <= elapsed_time < 11:
            car.set_accel(-9)
        elif 11 <= elapsed_time < 26:
            car.set_accel(4)
        elif 26 <= elapsed_time < 30:
            car.set_accel(0)
        elif 30 <= elapsed_time < 34:
            car.set_accel(-9)
        elif 34 <= elapsed_time < 38:
            car.set_accel(-4.5)
        elif 38 <= elapsed_time < 44:
            car.set_accel(-2)
        else:
            break
        ######################################################################
        ######################################################################

        car.update_state(time_step)
        elapsed_time += time_step
        iteration += 1

        # If animating the result, a low interval will result in potentially
        # extremely slow performance, as the animation figure will be updated
        # each time this function yields a value.
        if iteration % interval == 0:
            yield elapsed_time


if __name__ == "__main__":
    mode_defaults = {
        "square": {
            "amplitude": 0.03,
            "frequency": 0.1
        },
        "sine": {
            "amplitude": 0.3,
            "frequency": 0.04
        },
        "triangle": {
            "amplitude": 0.05,
            "frequency": 1.8
        },
        "bump": {
            "amplitude": 0.05,
            "frequency": 1.8
        }
    }

    argparser = argparse.ArgumentParser(usage='%(prog)s [options]\nWe have some defaults depending on --mode. ' + str(mode_defaults))
    argparser.add_argument("--mode", "-m", type=str, default="sine",
        choices=['flat', 'sine', 'square', 'triangle', 'bump'],
        help="Road profile mode: (default: %(default)s)"
    )
    argparser.add_argument("--amplitude", "-a", type=float,
        help="Amplitude (in meters) for given '--mode'"
    )
    argparser.add_argument("--frequency", "-f", type=float,
        help="Frequency for given '--mode'"
    )
    argparser.add_argument("--time-step", "-t", type=float, default=0.0005,
        help="Simulation time step in seconds (default: %(default)s)"
    )
    argparser.add_argument("--interval", "-i", type=int, default=100,
        help="Draw animation frame every <interval> time steps  (default: %(default)s)"
    )
    argparser.add_argument("--write", "-w", action="store_true",
        help="Write resulting animation to a video file"
    )

    args = {
        arg: val for arg, val in vars(argparser.parse_args()).items()
        if val is not None
    }

    # Set parameters for `Road` object.
    road_args = {
        "mode": args["mode"],
        "x_min": -3.3,
        "length": 6
    }

    # Apply `mode_defaults` for `Road` settings.
    if args["mode"] in ("sine", "square", "triangle", "bump"):
        road_args["amplitude"] = args.get("amplitude", mode_defaults[args["mode"]]["amplitude"])
        road_args["frequency"] = args.get("frequency", mode_defaults[args["mode"]]["frequency"])

    # Instantiate `Road` and `Car` objects, passing the `Road` object to the
    # `Car` constructor. Note that, if no road object is passed to the `Car`
    # constructor via the `road_func` keyword argument, the `Car` constructor
    # instantiates a `Road` object with certain default parameters.
    road = Road(**road_args)
    car = Car(road_func=road)

    # Create a `PlotSim` object, passing the `Car` object instantiated above.
    # Passing `True` for the `suspension` keyword argument ensures that the
    # car's suspension springs are drawn in the animation.
    plot_sim = PlotSim(car, suspension=True)

    # Create a generator from the generator function `simulate()` defined
    # in this example script.
    generator = simulate(
        car, time_step=args["time_step"], interval=args["interval"]
    )

    # Call the `PlotSim` object's `animate()` method, passing in the required
    # generator (which updates the `Car` object's state each time it's called).
    # The video write parameters are optional; if the `--write`/`-w` option was
    # not supplied when calling this script, no video will be written and the
    # video write arguments will be ignored.
    writer = "ffmpeg"
    fps = 1 / (args["time_step"] * args["interval"])
    writer_args = ["-vcodec", "h264"]

    plot_sim.animate(
        generator,
        write_video=args["write"], writer=writer, fps=fps, writer_args=writer_args
    )
