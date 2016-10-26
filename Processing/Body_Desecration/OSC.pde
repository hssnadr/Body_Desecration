/**
 * oscP5 website at http://www.sojamo.de/oscP5
 */
 
// SEND OSC MESSAGES
void newOSCMessage(String canal, float message) {
  /* create a new OscMessage with an address pattern, in this case /test. */
  OscMessage myOscMessage = new OscMessage("/" + canal);
  /* add a value (an integer) to the OscMessage */
  myOscMessage.add(message);
  /* send the OscMessage to a remote location specified in myNetAddress */
  oscP5.send(myOscMessage, myBroadcastLocation);
}
 
 
 
// RECEIVE OSC MESSAGES
void oscEvent(OscMessage theOscMessage) {
  /* check if theOscMessage has the address pattern we are looking for. */
  
  // GET ACCELERATION X VALUES
  if (theOscMessage.checkAddrPattern("/osc/x")) {
    /* check if the typetag is the right one. */
    if (theOscMessage.checkTypetag("f")) { //f=float, s = string, i = int ...
      ax = theOscMessage.get(0).floatValue() ;
      println("AccX = " +ax);
      isOSC = true;
      return;
    }
  }
  
  // GET ACCELERATION Y VALUES
  if (theOscMessage.checkAddrPattern("/osc/y")) {
    /* check if the typetag is the right one. */
    if (theOscMessage.checkTypetag("f")) { //f=float, s = string, i = int ...
      ay = theOscMessage.get(0).floatValue() ;
      println("AccY = " +ay);
      isOSC = true;
      return;
    }
  }
  
  println("### received an osc message. with address pattern "+theOscMessage.addrPattern()+" and typetag "+theOscMessage.typetag());
}