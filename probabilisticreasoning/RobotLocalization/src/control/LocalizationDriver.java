package control;

/*IMPORTANT NOTE
 * This file was implemented by the course responsibles for the course EDAP01 at LTH,
 * I take no credit in their work.
 */

import view.*;

public class LocalizationDriver extends Thread {
	
	private RobotLocalizationViewer l;
	long timer;
	
	public LocalizationDriver( long stepTime, RobotLocalizationViewer v) {
		this.l = v;
		this.timer = stepTime;
	}
	
	public void run() {
		while( !isInterrupted()) {
			
			
			try{
				l.updateContinuously();
				sleep( timer);
			} catch( InterruptedException e) {
				System.out.println( "oops");
			}

		}
	}
	
}