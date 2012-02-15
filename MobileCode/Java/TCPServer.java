import java.io.DataInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.net.Socket;

public class TCPServer implements Runnable {

	/**
	 * @param args
	 */
	
	private Socket SFserver;
	private MessageQueue queue;
	private PrintStream output;
	private DataInputStream input;
	
	public TCPServer (Socket server)
	{
		SFserver = server;
		queue = new MessageQueue();		

		try {
			output = new PrintStream (SFserver.getOutputStream());
			input = new DataInputStream (SFserver.getInputStream());
		} catch (IOException e) {
			e.printStackTrace();
		}		
	}
	
	public void run ()
	{
		byte [] b = new byte [0];
		
		try {
			int cmd = input.readInt();
			int len = input.readInt();
			
			input.read(b, 0, len);
			
			switch(cmd)
			{
			case CommandHeader.REQUEST_NUM_SHOPPING_LISTS:
				System.out.println ("hi num");
			case CommandHeader.REQUEST_SHOPPING_LIST:
				System.out.println ("list");
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
