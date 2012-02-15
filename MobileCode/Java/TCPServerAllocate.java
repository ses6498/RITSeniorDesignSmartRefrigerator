import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServerAllocate implements Runnable{

	private ServerSocket server;
	
	public TCPServerAllocate ()
	{
		try {
			server = new ServerSocket (1355, 0, InetAddress.getByName("127.0.0.1"));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void run ()
	{
		Socket sock = null;
		TCPServer serv;
		
		while (true)
		{
			try {
				sock = server.accept();
				serv = new TCPServer (sock);
				(new Thread (serv)).start();
			} catch (IOException e) {
				e.printStackTrace();
			}			
		}
	}
	
	public static void main(String[] args) {

		(new Thread (new TCPServerAllocate())).start();
		
		try {
			Thread.sleep(400);
			TCPClient c = new TCPClient ();
			Thread.sleep(400);
			(new Thread(c)).start();
			Thread.sleep(400);
			c.PostRequestNumShoppingLists();
			
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
}
