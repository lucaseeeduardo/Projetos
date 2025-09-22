import java.util.Comparator;

public class GameEntryComparator implements Comparator<GameEntry> {
    
     @Override
    public int compare(GameEntry entrada1, GameEntry entrada2) {
        return Integer.compare(entrada1.getScore(), entrada2.getScore());
    }
}
