import java.io.DataInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.net.InetAddress;
import java.net.Socket;

public class TCPClient implements Runnable {		
	private Socket SFclient;
	private DataInputStream input;
	private PrintStream output;
	
	private MessageQueue queue;
	
	public TCPClient ()
	{
		queue = new MessageQueue();
		
		try
		{
			SFclient = new Socket (InetAddress.getByName("127.0.0.1"), 1355);
			input = new DataInputStream (SFclient.getInputStream());
			output = new PrintStream (SFclient.getOutputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void run ()
	{
		MessageQueueElement msg;
		
		while (true)
		{
			queue.acquire();
			msg = queue.pop();
			
			output.write((int)(msg.header.id));
			output.write(msg.header.length);
			try {
				if (msg.header.length > 0)
				{
					output.write(msg.payload);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void PostRequestNumShoppingLists ()
	{
		MessageQueueElement msg = new MessageQueueElement ();
		
		msg.header.id = CommandHeader.REQUEST_NUM_SHOPPING_LISTS;
		msg.header.length = 0;
		msg.payload = null;
		
		queue.push(msg);
	}
}
