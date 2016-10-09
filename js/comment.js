// COMMENTS

var commentTemplate = "<div class='comment-box'><p>username</p><p>comment_text</p></div>"

function buildComment(commentTemplate, username, commentText) {
	var newComment = commentTemplate
			.replace('username', username)
			.replace('comment_text', commentText);
	return newComment
};


var accentColors = {
	'#f43c50': '#e03b55',
	'#3bb3e8': '#2b85ae',
	'#53de8a': '#3da567',
	'#e046f1': '#c93fda',
	'#f3dc4c': '#cdb942',
	'#282828': '#7b7b7b',
}

// VOTES



$(document).ready(function(e) {

	$('.comment-icon').on('click', function(e){
  		e.preventDefault();
  		console.log('hey girl');
  		$(this).parent().siblings('.comment-box').toggleClass('hide');
	});



	$('.comment-form').on('submit', function(e) {
		e.preventDefault();
		console.log('submit fired')

		var commentText = $(this).find('.new-comment-text').val();
		var haikuID = $(this).parent().attr('data-haikuid');
		var username = $('.menu-box h3').text();

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
				if (currentVoteCount == '') {
					var newVoteCount = 1
				} else {
					newVoteCount = parseInt(currentVoteCount) + 1
				}
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
		// $(this).addClass('selected').siblings().removeClass('selected');
		$('body').css('background', mainColor);
		$('input').css('background', accentColor);
		$('.color-option').css('z-index', 1000);
		$('.button').css('background', mainColor);
		$('.button').css('color', 'white');
	});
});

