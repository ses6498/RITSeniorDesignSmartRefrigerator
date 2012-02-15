public class MessageQueueElement {
	public CommandHeader header;
	public byte [] payload;
	
	public MessageQueueElement ()
	{
		header = new CommandHeader();
		payload = null;
	}
}