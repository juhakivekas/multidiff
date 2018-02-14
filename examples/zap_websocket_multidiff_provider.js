// Usage:
// Add script as Extender scipt in ZAP and enable it
// Edit the channelSelector function to include your target traffic
//   multidiff -i json -p 8000
// point your browser to ZAP and open some websocket application

var Socket = Java.type("java.net.Socket")
var Base64 = Java.type("java.util.Base64")

/**
 * Select websocket channels to be included based on the handshake message
 */
function channelSelector(handshakeReference){
	return handshakeReference.getURI().getHost().matches('.*firebase.*')
}
/**
 * Filter out interesting messages or to weed out junk
 */
function messageSelector(message){
	return true
}
/**
 * Do any cropping, formatting, etc. to a message before sending to multidiff
 */
function getData(message){
	return JSON.stringify(JSON.parse(message.getReadablePayload()), null, 2).getBytes()
	//return message.getPayload()
}

/**** support functions follow *****/

/**
 * ECMA implementation of WebSocketSenderListener that sends WebSocket messages to the multidiff server
 */
var scope = []
var tamperListener = new org.zaproxy.zap.extension.websocket.WebSocketSenderListener(){
	getListenerOrder: function(){
		return 10;
	},
	onMessageFrame: function(channelId, message, initiator){
		if(scope.indexOf(channelId) < 0){return}
		if(!messageSelector(message)){return}
		if(message.getDirection() == org.zaproxy.zap.extension.websocket.WebSocketMessage.Direction.OUTGOING){
			direction = "\u25b6"
		} else {
			direction = "\u25c0"
		}
		diffobj = JSON.stringify({
			'data' : Base64.getEncoder().encodeToString(getData(message)),
			'info' : direction + ' ' + channelId + '.' + message.getMessageId()
		})
		diffsocket = new Socket("localhost", 8000)
		diffstream = diffsocket.getOutputStream()
		diffstream.write(diffobj.getBytes())
		diffstream.close()
	},
	onStateChange: function(state, proxy){
		if(state == 'OPEN'){
			if(channelSelector(proxy.getHandshakeReference())){
				scope.push(proxy.getChannelId())
				action = 'hook'
			} else {
				action = 'skip'
			}
			host = proxy.getHandshakeReference().getURI().getHost()
			print(action +' #' + proxy.getChannelId() + ':' + host)
		}
	}
}

/**
 * This function is called when the script is enabled, it adds the custom WebSocketSenderListener object to the WebSocket extension.
 */
function install(helper) {
	extensionWebSocket = org.parosproxy.paros.control.Control.getSingleton().getExtensionLoader().getExtension(
		org.zaproxy.zap.extension.websocket.ExtensionWebSocket.NAME)
	extensionWebSocket.addAllChannelSenderListener(tamperListener)
	//note that the listener will not be attached to already existing WebSocket connections
	//reloading pages to reconnect all sockets might be needed to enable the added listener
}

/**
 * This function is called when the script is disabled, it removes the custom WebSocketSenderListener object to the WebSocket extension.
 */
function uninstall(helper) {
	extensionWebSocket = org.parosproxy.paros.control.Control.getSingleton().getExtensionLoader().getExtension(
		org.zaproxy.zap.extension.websocket.ExtensionWebSocket.NAME)
	extensionWebSocket.removeAllChannelSenderListener(tamperListener)
}
