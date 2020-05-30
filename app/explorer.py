import flask

from app import api
from app import explorer


# The default IR to display.
DEFAULT_IRS = {
  "clang": """\
int Fib(int x) {
    switch(x) {
        case 0:
            return 0;
        case 1:
            return 1;
        default:
            return Fib(x - 1) + Fib(x - 2);
  }
}
""",
  "llvm": """\
source_filename = "example.c"

define i32 @Fib(i32) local_unnamed_addr #0 {
  switch i32 %0, label %3 [
    i32 0, label %9
    i32 1, label %2
  ]

; <label>:2:
  br label %9

; <label>:3:
  %4 = add nsw i32 %0, -1
  %5 = tail call i32 @Fib(i32 %4)
  %6 = add nsw i32 %0, -2
  %7 = tail call i32 @Fib(i32 %6)
  %8 = add nsw i32 %7, %5
  ret i32 %8

; <label>:9:
  %10 = phi i32 [ 1, %2 ], [ %0, %1 ]
  ret i32 %10
}
""",
  "xla": """\
hlo_module {
  name: "cluster_0__XlaCompiledKernel_true__XlaNumConstantArgs_3__XlaNumResourceArgs_0_.76"
  entry_computation_name: "cluster_0__XlaCompiledKernel_true__XlaNumConstantArgs_3__XlaNumResourceArgs_0_.76"
  computations {
    name: "max_float_.13"
    instructions {
      name: "x.14"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 14
    }
    instructions {
      name: "y.15"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      parameter_number: 1
      id: 15
    }
    instructions {
      name: "maximum.16"
      opcode: "maximum"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 16
      operand_ids: 14
      operand_ids: 15
    }
    program_shape {
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      result {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameter_names: "x.14"
      parameter_names: "y.15"
    }
    id: 13
    root_id: 16
  }
  computations {
    name: "add_float_.23"
    instructions {
      name: "x.24"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 24
    }
    instructions {
      name: "y.25"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      parameter_number: 1
      id: 25
    }
    instructions {
      name: "add.26"
      opcode: "add"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 26
      operand_ids: 24
      operand_ids: 25
    }
    program_shape {
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      result {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameter_names: "x.24"
      parameter_names: "y.25"
    }
    id: 23
    root_id: 26
  }
  computations {
    name: "gradients_Softmax_grad_Sum-reduction.49"
    instructions {
      name: "x.50"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 50
    }
    instructions {
      name: "y.51"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      parameter_number: 1
      id: 51
    }
    instructions {
      name: "add.52"
      opcode: "add"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 52
      operand_ids: 50
      operand_ids: 51
    }
    program_shape {
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      result {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameter_names: "x.50"
      parameter_names: "y.51"
    }
    id: 49
    root_id: 52
  }
  computations {
    name: "gradients_add_grad_Sum_1-reduction.63"
    instructions {
      name: "x.64"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 64
    }
    instructions {
      name: "y.65"
      opcode: "parameter"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      parameter_number: 1
      id: 65
    }
    instructions {
      name: "add.66"
      opcode: "add"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
      }
      id: 66
      operand_ids: 64
      operand_ids: 65
    }
    program_shape {
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameters {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      result {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      parameter_names: "x.64"
      parameter_names: "y.65"
    }
    id: 63
    root_id: 66
  }
  computations {
    name: "cluster_0__XlaCompiledKernel_true__XlaNumConstantArgs_3__XlaNumResourceArgs_0_.76"
    instructions {
      name: "arg2.3"
      opcode: "parameter"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 784
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Args"
      }
      parameter_number: 2
      id: 3
      parameter_replication {
        replicated_at_leaf_buffers: false
      }
    }
    instructions {
      name: "reshape.7"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 784
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
      }
      id: 7
      operand_ids: 3
    }
    instructions {
      name: "arg0.1"
      opcode: "parameter"
      shape {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Args"
      }
      id: 1
      parameter_replication {
        replicated_at_leaf_buffers: false
      }
    }
    instructions {
      name: "reshape.5"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
      }
      id: 5
      operand_ids: 1
    }
    instructions {
      name: "dot.9"
      opcode: "dot"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "MatMul"
        op_name: "MatMul"
      }
      dot_dimension_numbers {
        lhs_contracting_dimensions: 1
        rhs_contracting_dimensions: 0
      }
      id: 9
      operand_ids: 7
      operand_ids: 5
      precision_config {
        operand_precision: DEFAULT
        operand_precision: DEFAULT
      }
    }
    instructions {
      name: "arg1.2"
      opcode: "parameter"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Args"
      }
      parameter_number: 1
      id: 2
      parameter_replication {
        replicated_at_leaf_buffers: false
      }
    }
    instructions {
      name: "reshape.6"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
      }
      id: 6
      operand_ids: 2
    }
    instructions {
      name: "broadcast.10"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Add"
        op_name: "add"
      }
      dimensions: 1
      id: 10
      operand_ids: 6
    }
    instructions {
      name: "add.11"
      opcode: "add"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Add"
        op_name: "add"
      }
      id: 11
      operand_ids: 9
      operand_ids: 10
    }
    instructions {
      name: "constant.12"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: -inf
      }
      id: 12
    }
    instructions {
      name: "reduce.17"
      opcode: "reduce"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      dimensions: 1
      id: 17
      operand_ids: 11
      operand_ids: 12
      called_computation_ids: 13
    }
    instructions {
      name: "broadcast.18"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      dimensions: 0
      id: 18
      operand_ids: 17
    }
    instructions {
      name: "subtract.19"
      opcode: "subtract"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      id: 19
      operand_ids: 11
      operand_ids: 18
    }
    instructions {
      name: "exponential.20"
      opcode: "exponential"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      id: 20
      operand_ids: 19
    }
    instructions {
      name: "convert.21"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      id: 21
      operand_ids: 20
    }
    instructions {
      name: "constant.22"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: 0
      }
      id: 22
    }
    instructions {
      name: "reduce.27"
      opcode: "reduce"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      dimensions: 1
      id: 27
      operand_ids: 21
      operand_ids: 22
      called_computation_ids: 23
    }
    instructions {
      name: "convert.28"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      id: 28
      operand_ids: 27
    }
    instructions {
      name: "broadcast.29"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      dimensions: 0
      id: 29
      operand_ids: 28
    }
    instructions {
      name: "divide.30"
      opcode: "divide"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Softmax"
        op_name: "Softmax"
      }
      id: 30
      operand_ids: 20
      operand_ids: 29
    }
    instructions {
      name: "log.31"
      opcode: "log"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Log"
        op_name: "Log"
      }
      id: 31
      operand_ids: 30
    }
    instructions {
      name: "arg3.4"
      opcode: "parameter"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Args"
      }
      parameter_number: 3
      id: 4
      parameter_replication {
        replicated_at_leaf_buffers: false
      }
    }
    instructions {
      name: "reshape.8"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
      }
      id: 8
      operand_ids: 4
    }
    instructions {
      name: "multiply.32"
      opcode: "multiply"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Mul"
        op_name: "mul"
      }
      id: 32
      operand_ids: 31
      operand_ids: 8
    }
    instructions {
      name: "constant.41"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Reciprocal"
        op_name: "gradients/Log_grad/Reciprocal"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: 1
      }
      id: 41
    }
    instructions {
      name: "broadcast.42"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Reciprocal"
        op_name: "gradients/Log_grad/Reciprocal"
      }
      id: 42
      operand_ids: 41
    }
    instructions {
      name: "divide.43"
      opcode: "divide"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Reciprocal"
        op_name: "gradients/Log_grad/Reciprocal"
      }
      id: 43
      operand_ids: 42
      operand_ids: 30
    }
    instructions {
      name: "constant.34"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: 0
      }
      id: 34
    }
    instructions {
      name: "broadcast.35"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      id: 35
      operand_ids: 34
    }
    instructions {
      name: "constant.33"
      opcode: "constant"
      shape {
        element_type: F32
        dimensions: 1
        dimensions: 1
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      literal {
        shape {
          element_type: F32
          dimensions: 1
          dimensions: 1
          layout {
            minor_to_major: 1
            minor_to_major: 0
            format: DENSE
          }
          is_dynamic_dimension: false
          is_dynamic_dimension: false
        }
        f32s: -1
      }
      id: 33
    }
    instructions {
      name: "reshape.36"
      opcode: "reshape"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      id: 36
      operand_ids: 33
    }
    instructions {
      name: "broadcast.37"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      id: 37
      operand_ids: 36
    }
    instructions {
      name: "add.38"
      opcode: "add"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Tile"
        op_name: "gradients/Sum_grad/Tile"
      }
      id: 38
      operand_ids: 35
      operand_ids: 37
    }
    instructions {
      name: "multiply.39"
      opcode: "multiply"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Mul"
        op_name: "gradients/mul_grad/Mul_1"
      }
      id: 39
      operand_ids: 8
      operand_ids: 38
    }
    instructions {
      name: "reshape.40"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Reshape"
        op_name: "gradients/mul_grad/Reshape_1"
      }
      id: 40
      operand_ids: 39
    }
    instructions {
      name: "multiply.44"
      opcode: "multiply"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Mul"
        op_name: "gradients/Log_grad/mul"
      }
      id: 44
      operand_ids: 43
      operand_ids: 40
    }
    instructions {
      name: "multiply.45"
      opcode: "multiply"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Mul"
        op_name: "gradients/Softmax_grad/mul"
      }
      id: 45
      operand_ids: 30
      operand_ids: 44
    }
    instructions {
      name: "convert.46"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      id: 46
      operand_ids: 45
    }
    instructions {
      name: "constant.47"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: 0
      }
      id: 47
    }
    instructions {
      name: "convert.48"
      opcode: "convert"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      id: 48
      operand_ids: 47
    }
    instructions {
      name: "reduce.53"
      opcode: "reduce"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      dimensions: 1
      id: 53
      operand_ids: 46
      operand_ids: 48
      called_computation_ids: 49
    }
    instructions {
      name: "convert.54"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      id: 54
      operand_ids: 53
    }
    instructions {
      name: "reshape.55"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 1
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/Softmax_grad/Sum"
      }
      id: 55
      operand_ids: 54
    }
    instructions {
      name: "reshape.56"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sub"
        op_name: "gradients/Softmax_grad/sub"
      }
      id: 56
      operand_ids: 55
    }
    instructions {
      name: "broadcast.57"
      opcode: "broadcast"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sub"
        op_name: "gradients/Softmax_grad/sub"
      }
      dimensions: 0
      id: 57
      operand_ids: 56
    }
    instructions {
      name: "subtract.58"
      opcode: "subtract"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sub"
        op_name: "gradients/Softmax_grad/sub"
      }
      id: 58
      operand_ids: 44
      operand_ids: 57
    }
    instructions {
      name: "multiply.59"
      opcode: "multiply"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Mul"
        op_name: "gradients/Softmax_grad/mul_1"
      }
      id: 59
      operand_ids: 30
      operand_ids: 58
    }
    instructions {
      name: "convert.60"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/add_grad/Sum_1"
      }
      id: 60
      operand_ids: 59
    }
    instructions {
      name: "constant.61"
      opcode: "constant"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/add_grad/Sum_1"
      }
      literal {
        shape {
          element_type: F32
          layout {
            format: DENSE
          }
        }
        f32s: 0
      }
      id: 61
    }
    instructions {
      name: "convert.62"
      opcode: "convert"
      shape {
        element_type: F32
        layout {
          format: DENSE
        }
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/add_grad/Sum_1"
      }
      id: 62
      operand_ids: 61
    }
    instructions {
      name: "reduce.67"
      opcode: "reduce"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/add_grad/Sum_1"
      }
      dimensions: 0
      id: 67
      operand_ids: 60
      operand_ids: 62
      called_computation_ids: 63
    }
    instructions {
      name: "convert.68"
      opcode: "convert"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Sum"
        op_name: "gradients/add_grad/Sum_1"
      }
      id: 68
      operand_ids: 67
    }
    instructions {
      name: "reshape.69"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Reshape"
        op_name: "gradients/add_grad/Reshape_1"
      }
      id: 69
      operand_ids: 68
    }
    instructions {
      name: "reshape.73"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Retvals"
      }
      id: 73
      operand_ids: 69
    }
    instructions {
      name: "transpose.71"
      opcode: "transpose"
      shape {
        element_type: F32
        dimensions: 784
        dimensions: 100
        layout {
          minor_to_major: 0
          minor_to_major: 1
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "MatMul"
        op_name: "gradients/MatMul_grad/MatMul_1"
      }
      dimensions: 1
      dimensions: 0
      id: 71
      operand_ids: 7
    }
    instructions {
      name: "reshape.70"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "Reshape"
        op_name: "gradients/add_grad/Reshape"
      }
      id: 70
      operand_ids: 59
    }
    instructions {
      name: "dot.72"
      opcode: "dot"
      shape {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_type: "MatMul"
        op_name: "gradients/MatMul_grad/MatMul_1"
      }
      dot_dimension_numbers {
        lhs_contracting_dimensions: 1
        rhs_contracting_dimensions: 0
      }
      id: 72
      operand_ids: 71
      operand_ids: 70
      precision_config {
        operand_precision: DEFAULT
        operand_precision: DEFAULT
      }
    }
    instructions {
      name: "reshape.74"
      opcode: "reshape"
      shape {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      metadata {
        op_name: "XLA_Retvals"
      }
      id: 74
      operand_ids: 72
    }
    instructions {
      name: "tuple.75"
      opcode: "tuple"
      shape {
        element_type: TUPLE
        tuple_shapes {
          element_type: F32
          dimensions: 10
          layout {
            minor_to_major: 0
            format: DENSE
          }
          is_dynamic_dimension: false
        }
        tuple_shapes {
          element_type: F32
          dimensions: 784
          dimensions: 10
          layout {
            minor_to_major: 1
            minor_to_major: 0
            format: DENSE
          }
          is_dynamic_dimension: false
          is_dynamic_dimension: false
        }
      }
      metadata {
        op_name: "XLA_Retvals"
      }
      id: 75
      operand_ids: 73
      operand_ids: 74
    }
    program_shape {
      parameters {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      parameters {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      parameters {
        element_type: F32
        dimensions: 100
        dimensions: 784
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      parameters {
        element_type: F32
        dimensions: 100
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
      result {
        element_type: TUPLE
        tuple_shapes {
          element_type: F32
          dimensions: 10
          layout {
            minor_to_major: 0
            format: DENSE
          }
          is_dynamic_dimension: false
        }
        tuple_shapes {
          element_type: F32
          dimensions: 784
          dimensions: 10
          layout {
            minor_to_major: 1
            minor_to_major: 0
            format: DENSE
          }
          is_dynamic_dimension: false
          is_dynamic_dimension: false
        }
      }
      parameter_names: "arg0.1"
      parameter_names: "arg1.2"
      parameter_names: "arg2.3"
      parameter_names: "arg3.4"
    }
    id: 76
    root_id: 75
  }
  host_program_shape {
    parameters {
      element_type: F32
      dimensions: 784
      dimensions: 10
      layout {
        minor_to_major: 1
        minor_to_major: 0
        format: DENSE
      }
      is_dynamic_dimension: false
      is_dynamic_dimension: false
    }
    parameters {
      element_type: F32
      dimensions: 10
      layout {
        minor_to_major: 0
        format: DENSE
      }
      is_dynamic_dimension: false
    }
    parameters {
      element_type: F32
      dimensions: 100
      dimensions: 784
      layout {
        minor_to_major: 1
        minor_to_major: 0
        format: DENSE
      }
      is_dynamic_dimension: false
      is_dynamic_dimension: false
    }
    parameters {
      element_type: F32
      dimensions: 100
      dimensions: 10
      layout {
        minor_to_major: 1
        minor_to_major: 0
        format: DENSE
      }
      is_dynamic_dimension: false
      is_dynamic_dimension: false
    }
    result {
      element_type: TUPLE
      tuple_shapes {
        element_type: F32
        dimensions: 10
        layout {
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
      }
      tuple_shapes {
        element_type: F32
        dimensions: 784
        dimensions: 10
        layout {
          minor_to_major: 1
          minor_to_major: 0
          format: DENSE
        }
        is_dynamic_dimension: false
        is_dynamic_dimension: false
      }
    }
    parameter_names: "p0"
    parameter_names: "p1"
    parameter_names: "p2"
    parameter_names: "p3"
  }
  entry_computation_id: 76
  input_output_alias {
  }
  dynamic_parameter_binding {
  }
}
""",
}

ENDPOINTS = api.EnumerateIr2GraphJson()


def Explorer(urls):
  data = {
    "default_irs": DEFAULT_IRS,
    "endpoints": ENDPOINTS,
    "defaults": {
      "ir": DEFAULT_IRS["clang"],
      "lang": "clang",
      "version": "default",
      "programl_version": "default",
    },
  }
  urls["highlight_js"] = flask.url_for("static", filename="highlight.pack.js")
  urls["explorer_js"] = flask.url_for("static", filename="explorer.js")
  return flask.render_template("explorer.html", data=data, urls=urls)
