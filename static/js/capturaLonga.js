var videoElement = document.getElementById('capturLongaTela');
var downloadURL = document.getElementById('capturLongaTela-download-url');

var startRecording = document.getElementById('capturLongaTela-start-recording');
var stopRecording = document.getElementById('capturLongaTela-stop-recording');

var eTimeOfRecording = '';
if (document.getElementById('CRCapturaLongaTempo')){
	eTimeOfRecording = document.getElementById('CRCapturaLongaTempo');
}




startRecording.onclick = function() {
	//indicadores de envio, barra de status
	$('.meter.capturLongaTela').css( "width", "0%" );
	$('.metertext.capturLongaTela').html("0%");
	
	//desabilitamos o botão de envio
	//ao final liberamos o envio
	$("#botaoSalvarVideoLongo").prop('disabled', true);
	
	$("#capturLongaTela-start-recording").prop('disabled', true);
	$("#capturLongaTela-stop-recording").prop('disabled', false);

	captureUserMedia(function(stream) {
		window.audioVideoRecorder = window.RecordRTC(stream, {
			type : 'video', // don't forget this; otherwise you'll get
							// video/webm instead of audio/ogg
			video_width : 240,
			video_height : 180,
			canvas_width : 240,
			canvas_height : 180,
			frameRate : 10,
			quality : 1,
		});
		try{
			timeOfRecording = eTimeOfRecording.options[eTimeOfRecording.selectedIndex].value;
		}catch(e){
			timeOfRecording = document.getElementById("formGravacaoVideoLongo").elements['tempoGravacao'].value;
		}
		window.audioVideoRecorder.startRecording();
		setTimeout(stopRecord, timeOfRecording);
	});
};

stopRecording.onclick = function() {
	stopRecord();
};

function stopRecord() {
	$("#capturLongaTela-start-recording").prop('disabled', false);
	$("#capturLongaTela-stop-recording").prop('disabled', true);

	window.audioVideoRecorder
			.stopRecording(function(url) {
				//ao final liberamos o envio
				$("#botaoSalvarVideoLongo").prop('disabled', false);
				
				downloadURL.innerHTML = '<a href="'
						+ url
						+ '" download="'+ document.getElementById("formGravacaoVideoLongo").elements['frase'].value
						+'.webm" target="_blank">Faça o Download do video para seu computador!</a>'; //setamos o nome do video
				videoElement.src = url;
				videoElement.muted = false;
				videoElement.loop = true;
				videoElement.play();

				videoElement.onended = function() {
					videoElement.pause();

					// dirty workaround for: "firefox seems unable to playback"
					videoElement.src = URL.createObjectURL(audioVideoRecorder
							.getBlob());
					
				};
			});
}

function captureUserMedia(callback) {
	navigator.getUserMedia = navigator.mozGetUserMedia
			|| navigator.webkitGetUserMedia 
			|| navigator.msGetUserMedia
			|| navigator.getUserMedia;
	navigator.getUserMedia({
		audio : true,
		video : true,
		video : {
			width : 240,
			height : 180
		},
		canvas : {
			width : 240,
			height : 180
		},
	}, function(stream) {
		videoElement.src = URL.createObjectURL(stream);
		videoElement.muted = true;
		videoElement.controls = true;
		videoElement.play();

		callback(stream);
	}, function(error) {
		console.error(error);
	});
}