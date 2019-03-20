from active_projects.ode.part1.pendulum import *
from active_projects.ode.part1.staging import *

OUTPUT_DIRECTORY = "ode/part1"
ALL_SCENE_CLASSES = [
    IntroducePendulum,
    FormulasAreLies,
    HighAnglePendulum,
    MediumAnglePendulum,
    LowAnglePendulum,
    ApproxWordsLowAnglePendulum,
    FailedApproxWordsHighAnglePendulum,
    # Tests
    PendulumTest,
    VectorFieldTest,
]
