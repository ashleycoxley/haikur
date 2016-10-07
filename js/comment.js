var commentTemplate = "<div class='comment-box'><p>username</p><p>comment_text</p></div>"

function buildComment(commentTemplate, username, commentText) {
	var newComment = commentTemplate
			.replace('username', username)
			.replace('comment_text', commentText);
	return newComment
};

$(document).ready(function() {
	$('.comment-form').on('submit', function(event) {
		event.preventDefault();

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
  		$(this).parent().siblings('.comment-box').toggleClass('hide');
	});
});

