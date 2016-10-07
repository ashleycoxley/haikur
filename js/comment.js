// COMMENTS

var commentTemplate = "<div class='comment-box'><p>username</p><p>comment_text</p></div>"

function buildComment(commentTemplate, username, commentText) {
	var newComment = commentTemplate
			.replace('username', username)
			.replace('comment_text', commentText);
	return newComment
};


// VOTES




$(document).ready(function(e) {
	$('.comment-form').on('submit', function(event) {
		e.preventDefault();

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

	$('.comment-icon').on('click', function(e){
  		e.preventDefault();
  		console.log('hey girl');
  		$(this).parent().siblings('.comment-box').toggleClass('hide');
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
			return;
			// var status = response.status
			// if (status == 'success') {
			// 	var voteObject = voteInstance.parent().siblings('.vote-count')
			// 	var voteCount = parseInt(voteObject.val());
			// 	voteCount += 1;
			// 	voteObject.val(voteCount.toString());
		});
		
 	});
});

