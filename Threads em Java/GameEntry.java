
public class GameEntry {

    @Override
    public String toString() {
        return String.format("Nome: %s | Pontuação: %d\n", name, score);
    }

    public GameEntry(String name, int score) {
        this.name = name;
        this.score = score;
    }

    public GameEntry(String name) {
        this.name = name;
    }

    public GameEntry() {
    }

    public String name;
    public int score;
    
    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
    
}
