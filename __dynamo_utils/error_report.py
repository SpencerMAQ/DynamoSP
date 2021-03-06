# copied from ladybug tools


"""Report errors"""
importErr, runErr   = IN
errors              = []

if importErr and str(importErr).startswith("ERROR:"):
    errors.append(importErr)

if runErr and str(runErr).startswith("ERROR:"):
    errors.append(runErr)

if len(errors) == 0:
    OUT = "All good! Vvizzzz."
else:
    OUT = "\n".join(errors)
