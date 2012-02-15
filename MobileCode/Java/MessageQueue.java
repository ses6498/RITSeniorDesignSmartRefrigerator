import java.util.concurrent.Semaphore;
import java.util.LinkedList;
import java.util.Queue;

public class MessageQueue {
	private Queue <MessageQueueElement> queue;
	public Semaphore queueSema;
	
	public MessageQueue ()
	{
		queue = new LinkedList <MessageQueueElement>();
		queueSema = new Semaphore(0);
	}
	
	public void acquire ()
	{
		try {
			queueSema.acquire();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void release ()
	{
		queueSema.release(1);
	}
	
	public void push (MessageQueueElement e)
	{
		queue.add(e);
		queueSema.release(1);
	}
	
	public MessageQueueElement pop ()
	{
		return queue.remove();
	}
}