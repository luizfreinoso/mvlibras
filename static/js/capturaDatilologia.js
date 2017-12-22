var videoElement = document.getElementById('DatilologiaViasualTela');
//var downloadURL = document.getElementById('capturaDatilologia-download-url');

var startRecording = document.getElementById('capturDatilologiaTela-start-recording');
var stopRecording = document.getElementById('capturDatilologiaTela-stop-recording');

var eTimeOfRecording = '';
if (document.getElementById('DVTempo')){
	eTimeOfRecording = document.getElementById('DVTempo');
}

startRecording.onclick = function() {
	if(document.getElementById("RDatilologiaVisual").elements['RDVResposta'].value != ""){
		//indicadores de envio, barra de status
		$('.meter.capturLongaTela').css( "width", "0%" );
		$('.metertext.capturLongaTela').html("0%");
		
		//desabilitamos o botão de envio
		//ao final liberamos o envio
		$("#botaoSalvarVideoDatilologia").prop('disabled', true);
		
		$("#capturDatilologiaTela-start-recording").prop('disabled', true);
		$("#capturDatilologiaTela-stop-recording").prop('disabled', false);
	
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
			timeOfRecording = eTimeOfRecording.options[eTimeOfRecording.selectedIndex].value;
			window.audioVideoRecorder.startRecording();
			setTimeout(stopRecord, timeOfRecording);
		});
	}else{
		alert('Insira a RESPOSTA para sua datilologia antes de gravar!');
	}
};

stopRecording.onclick = function() {
	stopRecord();
};

function stopRecord() {
	$("#capturDatilologiaTela-start-recording").prop('disabled', false);
	$("#capturDatilologiaTela-stop-recording").prop('disabled', true);

	window.audioVideoRecorder
			.stopRecording(function(url) {
				//ao final liberamos o envio
				$("#botaoSalvarVideoDatilologia").prop('disabled', false);
				
				//downloadURL.innerHTML = '<a href="'
				//		+ url
				//		+ '" download="'+ 'videoDatilologiaVIsual'
				//		+'.webm" target="_blank">Faça o Download do video para seu computador!</a>'; //setamos o nome do video
				videoElement.src = url;
				videoElement.muted = false;
				videoElement.loop = true;
				videoElement.play();

				videoElement.onended = function() {
					videoElement.pause();

					// dirty workaround for: "firefox seems unable to playback"
					videoElement.src = URL.createObjectURL(window.audioVideoRecorder
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