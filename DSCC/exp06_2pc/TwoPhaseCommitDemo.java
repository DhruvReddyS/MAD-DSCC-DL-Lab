public class TwoPhaseCommitDemo {
    // Phase 1: each participant receives PREPARE and votes YES/NO
    static boolean prepare(String node, boolean vote) {
        System.out.println(node + " received PREPARE, voted " + (vote ? "YES" : "NO"));
        return vote;
    }

    // Coordinator: commit only if every participant voted YES
    static void transaction(String[] nodes, boolean[] votes) {
        System.out.println("--- Phase 1: Prepare ---");
        boolean allYes = true;
        for (int i = 0; i < nodes.length; i++)
            allYes &= prepare(nodes[i], votes[i]);
        System.out.println("--- Phase 2: " + (allYes ? "Commit" : "Rollback") + " ---");
        for (String n : nodes)
            System.out.println(n + (allYes ? " COMMITTED" : " ROLLED BACK"));
    }

    public static void main(String[] args) {
        String[] nodes = {"Node1", "Node2", "Node3"};
        System.out.println("Transaction 1:");
        transaction(nodes, new boolean[]{true, true, true});
        System.out.println("\nTransaction 2:");
        transaction(nodes, new boolean[]{true, false, true});
    }
}
