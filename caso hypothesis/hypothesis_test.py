from hypothesis import given, settings, strategies as st
from hypothesis.extra.numpy import arrays
import numpy as np
from skimage.filters.ridges import frangi
from pypar import DynamicParallelizer, print_parallelizables, print_rewrite


# Strategy to generate 2D float arrays of reasonable size (to stress the function)
image_strategy = arrays(
    dtype=np.float64,
    shape=st.tuples(st.integers(1024, 4096), st.integers(1024, 4096)),
    elements=st.floats(min_value=0.0, max_value=1.0),
)

# Limit how many examples Hypothesis runs (each one runs PyPar)
@settings(max_examples=2, deadline=None)
@given(image=image_strategy)
def test_frangi_with_pypar(image):
    # Frangi execution
    print(f"\n[Running PyPar on image of shape: {image.shape}]")
    sigmas = np.linspace(1, 10, 5)
    code = 'frangi(image, sigmas=sigmas)'

    # Feed into PyPar
    parallelizer = DynamicParallelizer(
        code=code,
        glbs=globals(),
        lcls=locals()
    )

    # Print discovered parallelisms
    print_parallelizables(parallelizer)

    # Show rewritten parallel code for task 0 (if available)
    try:
        #print("\n\n\nHere is the rewrite\n\n\n")
        print_rewrite(parallelizer, 0)
    except Exception as e:
        print(f"[Warning] Could not rewrite code: {e}")

# Actually run the test
test_frangi_with_pypar()