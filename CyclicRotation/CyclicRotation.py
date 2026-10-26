class Solution {
    public int[] solution(int[] A, int K) {
        int N = A.length;

        if (N == 0) {
            return A;
        }

        int[] result = new int[N];
        K = K % N;

        for (int i = 0; i < N; i++) {
            int newIndex = (i + K) % N;
            result[newIndex] = A[i];
        }

        return result;
    }
}
