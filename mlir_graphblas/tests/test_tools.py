import pytest
import subprocess
import mlir_graphblas

TEST_CASES = (
    pytest.param(
        """
module  {
  func @test_func(%arg0: tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], pointerBitWidth = 64, indexBitWidth = 64 }>>) -> tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], pointerBitWidth = 64, indexBitWidth = 64 }>> {
    return %arg0 : tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], pointerBitWidth = 64, indexBitWidth = 64 }>>
  }
}
""",
        """
#CSX64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "dense", "compressed" ], 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

module  {
  func @test_func(%arg0: tensor<2x3xf64, #CSX64>) -> tensor<2x3xf64, #CSX64> {
    return %arg0 : tensor<2x3xf64, #CSX64>
  }
}
""",
        id="csx",
    ),
    pytest.param(
        """
module  {
  func @test_func(%arg0: tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>>) -> tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>> {
    return %arg0 : tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>>
  }
}
""",
        """
#CSC64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "dense", "compressed" ], 
    dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

module  {
  func @test_func(%arg0: tensor<2x3xf64, #CSC64>) -> tensor<2x3xf64, #CSC64> {
    return %arg0 : tensor<2x3xf64, #CSC64>
  }
}
""",
        id="csc",
    ),
    pytest.param(
        """
module  {
  func @test_func(%arg0: tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, pointerBitWidth = 64, indexBitWidth = 64 }>>) -> tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, pointerBitWidth = 64, indexBitWidth = 64 }>> {
    return %arg0 : tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, pointerBitWidth = 64, indexBitWidth = 64 }>>
  }
}
""",
        """
#CSR64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "dense", "compressed" ], 
    dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

module  {
  func @test_func(%arg0: tensor<2x3xf64, #CSR64>) -> tensor<2x3xf64, #CSR64> {
    return %arg0 : tensor<2x3xf64, #CSR64>
  }
}
""",
        id="csr",
    ),
    pytest.param(
        """
module  {
  func @convert_layout_wrapper(%arg0: tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, pointerBitWidth = 64, indexBitWidth = 64 }>>) -> tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>> {
    %0 = graphblas.convert_layout %arg0 : tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, pointerBitWidth = 64, indexBitWidth = 64 }>> to tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>>
    return %0 : tensor<2x3xf64, #sparse_tensor.encoding<{ dimLevelType = [ "dense", "compressed" ], dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, pointerBitWidth = 64, indexBitWidth = 64 }>>
  }
}
""",
        """
#CSC64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "dense", "compressed" ], 
    dimOrdering = affine_map<(d0, d1) -> (d1, d0)>, 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

#CSR64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "dense", "compressed" ], 
    dimOrdering = affine_map<(d0, d1) -> (d0, d1)>, 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

module  {
  func @convert_layout_wrapper(%arg0: tensor<2x3xf64, #CSR64>) -> tensor<2x3xf64, #CSC64> {
    %0 = graphblas.convert_layout %arg0 : tensor<2x3xf64, #CSR64> to tensor<2x3xf64, #CSC64>
    return %0 : tensor<2x3xf64, #CSC64>
  }
}
""",
        id="csr_and_csc",
    ),
    pytest.param(
        """
module  {
  func @vector_argminmax_min(%arg0: tensor<3xi64, #sparse_tensor.encoding<{ dimLevelType = [ "compressed" ], pointerBitWidth = 64, indexBitWidth = 64 }>>) -> index {
    %0 = graphblas.vector_argminmax %arg0 {minmax = "min"} : tensor<3xi64, #sparse_tensor.encoding<{ dimLevelType = [ "compressed" ], pointerBitWidth = 64, indexBitWidth = 64 }>>
    return %0 : index
  }
}
""",
        """
#SparseVec64 = #sparse_tensor.encoding<{ 
    dimLevelType = [ "compressed" ], 
    pointerBitWidth = 64, 
    indexBitWidth = 64 
}>

module  {
  func @vector_argminmax_min(%arg0: tensor<3xi64, #SparseVec64>) -> index {
    %0 = graphblas.vector_argminmax %arg0 {minmax = "min"} : tensor<3xi64, #SparseVec64>
    return %0 : index
  }
}
""",
        id="SparseVec64",
    ),
)


@pytest.mark.parametrize("input_mlir, output_mlir", TEST_CASES)
def test_tersify_mlir(input_mlir, output_mlir):
    """Check that the tersify_mlir CLI tool works."""
    process = subprocess.run(
        ["tersify_mlir"],
        capture_output=True,
        input=input_mlir.encode(),
    )
    assert process.returncode == 0
    stdout = process.stdout.decode().strip()
    assert stdout == output_mlir.strip()
    assert stdout == mlir_graphblas.tools.tersify_mlir(input_mlir).strip()
    return


def test_tersify_mlir_with_invalid_mlir():
    input_mlir = "asdf"
    process = subprocess.run(
        ["tersify_mlir"],
        capture_output=True,
        input=input_mlir.encode(),
    )
    assert process.returncode != 0
    assert len(process.stdout) == 0
    assert input_mlir in process.stderr.decode()
    return
