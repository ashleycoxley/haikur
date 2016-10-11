// COMMENTS

var commentTemplate = "<div class='comment-box'><p>username</p><p>comment_text</p></div>"

function buildComment(commentTemplate, username, commentText) {
	var newComment = commentTemplate
			.replace('username', username)
			.replace('comment_text', commentText);
	return newComment
};


var accentColors = {
	'#f24962': '#e03b55',
	'#44bfea': '#2b85ae',
	'#61e296': '#3da567',
	'#da65ef': '#c93fda',
	'#f4e067': '#cdb942',
	'#282828': '#7b7b7b',
}


function getSelfUsername() {
	return $.trim($('.menu-box h3').text());
}

function voterInvalid(voteInstance) {
	var selfUsername = getSelfUsername();
	var haikuUsername = voteInstance
		.parent()
		.parent()
		.parent()
		.siblings('.username-section')
		.find('p')
		.text();
	if (selfUsername == haikuUsername) {
		return true;
	}
};

// VOTES



$(document).ready(function(e) {

	$('.comment-icon').on('click', function(e){
  		e.preventDefault();
  		$(this).parent().siblings('.comment-box').toggleClass('hide');
	});



	$('.comment-form').on('submit', function(e) {
		e.preventDefault();

		var commentText = $(this).find('.new-comment-text').val();
		var haikuID = $(this).parent().attr('data-haikuid');
		var username = getSelfUsername();

		var data = {
			'commentText': commentText,
			'haikuID': haikuID
		};

		var commentUrl = '/' + haikuID + '/comment';
		var commentPost = $.post(commentUrl, data);

		var newComment = buildComment(commentTemplate, username, commentText)

		$(this).children('.comment-form-box').children('.new-comment-text').val('');
		var commentList = $(this).parent().siblings('.comment-list');
		commentPost.done(function() {
			commentList.append(newComment);
		});	
	});



	$('.vote-icon').on('click', function(e) {
		e.preventDefault();
		var voteInstance = $(this)

		// Check that voter is not author of haiku
		if (voterInvalid(voteInstance)) {
			return;
		}
		
		var haikuID = voteInstance.parent().parent().attr('data-haikuid');
		var voteType = voteInstance.attr('id');
		var voteUrl = '/' + haikuID + '/vote';

		if (voteType == 'upvote') {
			var voteType = 'upvote';
		} else if (voteType == 'downvote') {
			var voteType = 'downvote';
		}

		var data = {
			'haikuID': haikuID,
			'voteType': voteType
		};

		var votePost = $.post(voteUrl, data, function(response) {
			console.log(response)
			console.log(JSON.parse(response).change)
			response = JSON.parse(response)
			if (response.change == 'current_increment') {
				var currentSrc = voteInstance.attr('src').slice(0, -4)
				voteInstance.attr('src', currentSrc + '_selected.png')
				var currentVoteCount = voteInstance.siblings('.vote-count').text()
				console.log('current vote count:', currentVoteCount)
				if (currentVoteCount == '') {
					var newVoteCount = 1
				} else {
					newVoteCount = parseInt(currentVoteCount) + 1
				}
				console.log('new vote count:', newVoteCount)
				voteInstance.siblings('.vote-count').text(newVoteCount)

			} else if (response.change == 'current_decrement') {
				var currentSrc = voteInstance.attr('src').slice(0, -13)
				voteInstance.attr('src', currentSrc + '.png')
				var currentVoteCount = voteInstance.siblings('.vote-count').text()
				if (currentVoteCount == '1') {
					var newVoteCount = ''
				} else {
					newVoteCount = parseInt(currentVoteCount) - 1
				}
				voteInstance.siblings('.vote-count').text(newVoteCount)

			} else if (response.change == 'switch') {
				var currentSrc = voteInstance.attr('src').slice(0, -4)
				voteInstance.attr('src', currentSrc + '_selected.png')
				var currentVoteCount = voteInstance.siblings('.vote-count').text()
				if (currentVoteCount == '') {
					var newVoteCount = 1
				} else {
					newVoteCount = parseInt(currentVoteCount) + 1
				}
				voteInstance.siblings('.vote-count').text(newVoteCount)

				otherInstance = voteInstance.parent().siblings('.vote-box').children('.vote-icon')
				var otherSrc = otherInstance.attr('src').slice(0, -13)
				otherInstance.attr('src', otherSrc + '.png')
				var otherVoteCount = otherInstance.siblings('.vote-count').text()
				console.log(otherVoteCount)
				if (otherVoteCount == '1') {
					var newOtherVoteCount = ''
				} else {
					newOtherVoteCount = parseInt(otherVoteCount) - 1
				}
				console.log(newOtherVoteCount)
				otherInstance.siblings('.vote-count').text(newOtherVoteCount)
			}
		});
		
 	});



	$('input[type="radio"]').on('click', function(e) {
		var mainColor = $(this).parent().data('color');
		var accentColor = accentColors[mainColor];
		$('body').css('background', mainColor);
		$('.color-box').css('background', mainColor);
		$('input').css('background', accentColor);
		$('.button').css('background', mainColor);
		$('.button').css('color', 'white');
	});
});

