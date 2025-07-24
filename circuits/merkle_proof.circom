pragma circom 2.1.4;

include "../node_modules/circomlib/circuits/poseidon.circom";
include "../node_modules/circomlib/circuits/comparators.circom";

template MerkleProof(depth) {
    signal input leaf;
    signal input path_elements[depth];
    signal input path_index[depth];
    signal input root;

    signal output isValid;

    signal cur[depth + 1];
    cur[0] <== leaf;

    // Khai báo mảng tín hiệu ở cấp độ cao nhất
    signal left[depth];
    signal right[depth];
    signal temp1[depth];
    signal temp2[depth];
    signal temp3[depth];
    signal temp4[depth];
    signal temp5[depth];
    component h[depth];

    for (var i = 0; i < depth; i++) {
        // Khởi tạo component Poseidon
        h[i] = Poseidon(2);

        // Tính toán left[i]
        temp1[i] <== 1 - path_index[i];              // (1 - path_index[i])
        temp2[i] <== temp1[i] * cur[i];              // (1 - path_index[i]) * cur[i]
        temp3[i] <== path_index[i] * path_elements[i];  // path_index[i] * path_elements[i]
        left[i] <== temp2[i] + temp3[i];             // left[i] = temp2[i] + temp3[i]

        // Tính toán right[i]
        temp4[i] <== path_index[i] * cur[i];         // path_index[i] * cur[i]
        temp5[i] <== (1 - path_index[i]) * path_elements[i];  // (1 - path_index[i]) * path_elements[i]
        right[i] <== temp4[i] + temp5[i];            // right[i] = temp4[i] + temp5[i]

        // Gán đầu vào cho Poseidon
        h[i].inputs[0] <== left[i];
        h[i].inputs[1] <== right[i];

        // Cập nhật cur cho cấp tiếp theo
        cur[i + 1] <== h[i].out;
    }

    // Kiểm tra root
    signal diff;
    diff <== cur[depth] - root;

    // Sử dụng IsZero để kiểm tra diff == 0
    component isZero = IsZero();
    isZero.in <== diff;
    isValid <== isZero.out;
}

component main = MerkleProof(3);