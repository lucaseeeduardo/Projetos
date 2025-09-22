import java.util.ArrayList;
import java.util.List;


public class ProducerConsumer {
    public static void main(String[] args) {
        ProducerConsumer pc = new ProducerConsumer();
        var produtor = pc.new Producer();
        var consumidor = pc.new Consumer();

        try {
            produtor.produce(1);
            System.out.println("Produziu. Tamanho: " + pc.buffer.size());
            consumidor.consume();
            System.out.println("Consumiu. Tamanho: " + pc.buffer.size());
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private final List<Integer> buffer = new ArrayList<>(10);

    public class Producer {
        public void produce(int value) throws InterruptedException {
            synchronized (ProducerConsumer.this) {
                while (buffer.size() == 10) {
                    ProducerConsumer.this.wait();
                }
                buffer.add(value);
                System.out.println("buffer size: 10 | atual: " + buffer.size());
                ProducerConsumer.this.notifyAll();
            }
        }
    }

        /**
     * Consumes an item from the buffer. If the buffer is empty (count == 0), 
     * the calling thread waits until an item becomes available.
     * 
     * The method is synchronized to ensure thread safety when accessing the buffer.
     * 
     * After consuming an item, {@code notifyAll()} is called to wake up all waiting threads.
     * This is necessary because both producer and consumer threads may be waiting for changes 
     * in the buffer state. By notifying all, any waiting producer (waiting for space) or 
     * consumer (waiting for items) can re-check the buffer condition and proceed if possible.
     *
     * @return the consumed value from the buffer
     * @throws InterruptedException if the thread is interrupted while waiting
     */
    public class Consumer {
        /**
         * Consumes an item from the buffer.
         * <p>
         * This method removes and returns an item from the buffer. If the buffer is empty,
         * the calling thread waits until an item becomes available. After consuming an item,
         * it notifies all waiting threads that the buffer state has changed.
         * </p>
         *
         * @return the consumed item from the buffer
         * @throws InterruptedException if the thread is interrupted while waiting
         *
         * <p>
         * <b>Nota sobre o bloco synchronized:</b>
         * O bloco <code>synchronized5 (ProducerConsumer.this)</code> garante que apenas uma thread
         * por vez possa acessar a seção crítica do método, protegendo o acesso concorrente ao buffer
         * e à variável <code>count</code>. Isso evita condições de corrida e garante a consistência dos dados.
         * </p>
         */
        public int consume() throws InterruptedException {
            synchronized (ProducerConsumer.this) {
                while (buffer.isEmpty()) {
                    ProducerConsumer.this.wait();
                }
                int value = buffer.remove(buffer.size() - 1);
                System.out.println("buffer size: 10 | atual: " + buffer.size());
                ProducerConsumer.this.notifyAll();
                return value;
            }
        }
    }


}