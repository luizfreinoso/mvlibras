var videoElement = document.getElementById('capturaTela');
var downloadURL = document.getElementById('download-url');

var startRecording = document.getElementById('start-recording');
var stopRecording = document.getElementById('stop-recording');

startRecording.onclick = function() {
	//indicadores de envio, barra de status
	$('.meter').css( "width", "0%" );
	$('.metertext').html("0%");
	
	//desabilitamos o botão de envio
	//ao final liberamos o envio
	$("#botaoSalvarVideo").prop('disabled', true);
	
	$("#start-recording").prop('disabled', true);
	$("#stop-recording").prop('disabled', false);

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
		window.audioVideoRecorder.startRecording();
		setTimeout(stopRecord, 5700);
	});
};

stopRecording.onclick = function() {
	stopRecord();
};

function stopRecord() {
	$("#start-recording").prop('disabled', false);
	$("#stop-recording").prop('disabled', true);

	window.audioVideoRecorder
			.stopRecording(function(url) {
				//ao final liberamos o envio
				$("#botaoSalvarVideo").prop('disabled', false);
				
				downloadURL.innerHTML = '<a href="'
						+ url
						+ '" download="'+ document.getElementById("formGravacaoVideo").elements['palavra'].value
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
		audio : false,
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