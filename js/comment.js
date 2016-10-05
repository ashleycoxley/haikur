var commentTemplate = "<div class='comment-box'><p>username</p><p>comment_text</p></div>"

$(document).ready( function() {
	$('.comment-form').on('submit', function(event) {
		event.preventDefault();
		var commentText = $(this).find('.new-comment-text').val();
		var haikuID = $(this).parent().attr('data-haikuid');

		var data = {
			'commentText': commentText,
			'haikuID': haikuID
		};

		var username = $('.menu-box h3').text();
		var newComment = commentTemplate.replace('username', username).replace('comment_text', commentText);
		var commentUrl = '/' + haikuID + '/comment';
		var commentPost = $.post(commentUrl, data);

		$(this).children('.comment-form-box').children('.new-comment-text').val('');
		var commentList = $(this).parent().siblings('.comment-list');

		commentPost.done(function() {
			commentList.append(newComment);
		});
	});
});

