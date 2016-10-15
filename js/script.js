// HELPERS

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

// COMMENTS

var commentTemplate = "<div class='comment-container' data-commentid=COMMENT_ID>" +
	"	<p class='comment-username'>USERNAME</p>" +
	"	<p class='comment-text'>COMMENT_TEXT</p>" +
	"	<div class='comment-edit-box'>" +
	"		<img src='/assets/comment-delete.png' class='comment-edit-button comment-delete'>" +
	"		<img src='/assets/comment-edit.png' class='comment-edit-button comment-edit'>" +
	"	</div>" +
	"</div>"


function buildComment(commentTemplate, commentID, username, commentText) {
	var newComment = commentTemplate
			.replace('COMMENT_ID', commentID)
			.replace('USERNAME', username)
			.replace('COMMENT_TEXT', commentText);
	return newComment
};

var commentInputTemplate = "<form method='post'>" +
	"<div class='comment-form-box'>" +
	"	<textarea class='new-comment-text COLOR-accent'>COMMENT_TEXT</textarea>" +
	"</div>" +
	"<div class='form-footer'>" +
	"	<div class='button-box'>" +
	"		<img src='/assets/comments_close.png' class='comment-edit-button'>" +
	"		<input type='submit' value='SUBMIT EDIT' class='comment-edit-submit COLOR'>" +
	"	</div>" +
	"</div>" +
	"</form>"

function buildCommentEditBox(commentInputTemplate, commentText, color) {
	var commentEditBox = commentInputTemplate
		.replace('COMMENT_TEXT', commentText)
		.replace('COLOR', color)
		.replace('COLOR', color);
	return commentEditBox
}

function displayEditComment() {
	var commentEditInstance = $(this);
	var commentText = commentEditInstance
		.parent()
		.siblings('.comment-text')
		.text();
	var color = commentEditInstance
		.closest('.color-box')
		.attr('class')
		.split(' ')[1]
	var commentContainer = commentEditInstance
		.closest('.comment-container');

	var editBox = buildCommentEditBox(commentInputTemplate, commentText, color);

	commentContainer.empty();
	var editBoxDomElem = $(editBox);
	commentContainer.append(editBoxDomElem);
	
	$(editBoxDomElem).on('submit', editComment);
};


function editComment(e) {
	e.preventDefault();
	var username = getSelfUsername();
	var commentEditSubmitInstance= $(this);
	var commentContainer = commentEditSubmitInstance
		.closest('.comment-container');
	var commentID = commentContainer
		.attr('data-commentid');
	var haikuID = commentEditSubmitInstance
		.closest('.comment-list')
		.siblings('.comment-add')
		.attr('data-haikuid');
	var editedText = commentEditSubmitInstance
		.find('.new-comment-text')
		.val()
	var editCommentUrl = '/' + haikuID + '/comment/' + commentID + '/edit';
	var data = {
		'editedText': editedText
	}

	var newComment = buildComment(commentTemplate, commentID, username, editedText)
	editCommentPost = $.post(editCommentUrl, data)
	editCommentPost.done(function() {
		commentContainer.empty();
		commentContainer.append(newComment);
	});
};


function deleteComment() {
	var commentDeleteInstance = $(this);
	var commentID = commentDeleteInstance
		.closest('.comment-container')
		.attr('data-commentid');
	var haikuID = commentDeleteInstance
		.closest('.comment-list')
		.siblings('.comment-add')
		.attr('data-haikuid');

	var deleteCommentUrl = '/' + haikuID + '/comment/' + commentID + '/delete';
	var data = {
		'commentID': commentID
	}
	var votePost = $.post(deleteCommentUrl, data);
	votePost.done(function() {
		var commentCounter = commentDeleteInstance
			.closest('.comment-box')
			.siblings('.comment-header')
			.children('p');

		var commentCount = commentCounter.text()
		if (commentCount == 1) {
			commentCount = '';
		} else {
			commentCount = parseInt(commentCount) + 1;
		}
		commentCounter.text(commentCount)

		commentDeleteInstance
			.parent()
			.parent()
			.remove();
	});
};

function submitComment(e) {
	e.preventDefault();
	var commentInstance = $(this);

	// Assemble comment data for POST request
	var commentText = commentInstance.find('.new-comment-text').val();
	if (commentText == '') {
		return;
	}
	var haikuID = commentInstance.parent().attr('data-haikuid');
	var username = getSelfUsername();
	var data = {
		'commentText': commentText,
		'haikuID': haikuID
	};

	var commentUrl = '/' + haikuID + '/comment';
	var commentPost = $.post(commentUrl, data);

	commentPost.done(function(response) {
		response = JSON.parse(response)
		commentID = response['commentID']

		var newComment = buildComment(commentTemplate, commentID, username, commentText);
		commentInstance
			.children('.comment-form-box')
			.children('.new-comment-text')
			.val('');
		var commentList = commentInstance
			.parent()
			.siblings('.comment-list');
		commentPost.done(function() {
			var commentCounter = commentList
				.parent()
				.siblings('.comment-header')
				.children('p');
			var commentCount = commentCounter.text();
			if (commentCount == '') {
				commentCount = 1
			} else {
				commentCount = parseInt(commentCount) + 1
			}
			commentCounter.text(commentCount)
			commentList.append(newComment);
		});	
	});
};


// VOTING

function changeVote(voteInstance, changeType) {
	// set change variables for increment and decrement
	if (changeType == 'increment') {
		var idx1 = 0;
		var idx2 = -4;
		var filenameAddOn = '_selected.png'
		var incrementAmount = 1;
	} else if (changeType == 'decrement') {
		var idx1 = 0;
		var idx2 = -13;
		var filenameAddOn = '.png'
		var incrementAmount = -1;
	}
	// switch icon file name
	var currentSrc = voteInstance.attr('src').slice(idx1, idx2)
	voteInstance.attr('src', currentSrc + filenameAddOn)
	var currentVoteCount = voteInstance.siblings('.vote-count').text()

	// increment or decrement counter, setting 0 to an empty string
	if (currentVoteCount == '' && changeType == 'increment') {
		var newVoteCount = 1
	} else if (currentVoteCount == 1 && changeType == 'decrement') {
		var newVoteCount = ''
	} else {
		var newVoteCount = parseInt(currentVoteCount) + incrementAmount
	}

	voteInstance.siblings('.vote-count').text(newVoteCount)
};


function upvoteDownvote(e) {
	e.preventDefault();
	var voteInstance = $(this)

	// Check that voter is not author of haiku
	if (voterInvalid(voteInstance)) {
		return;
	}
		
	// Assemble voting data for POST request
	var haikuID = voteInstance.parent().parent().attr('data-haikuid');
	var voteType = voteInstance.attr('id');
	var voteUrl = '/' + haikuID + '/vote';
	var data = {
		'haikuID': haikuID,
		'voteType': voteType
	};

	// Post comment and change UI to reflect new comment
	var votePost = $.post(voteUrl, data, function(response) {
		response = JSON.parse(response)
		if (response.change == 'current_increment') {
			changeVote(voteInstance, 'increment');

		} else if (response.change == 'current_decrement') {
			changeVote(voteInstance, 'decrement');

		} else if (response.change == 'switch') {
			oppositeVoteInstance = voteInstance
				.parent()
				.siblings('.vote-box')
				.children('.vote-icon')
			changeVote(voteInstance, 'increment');
			changeVote(oppositeVoteInstance, 'decrement');
		}
	});
};


// SUBMIT / EDIT HAIKU

var accentColors = {
	'#f24962': '#e03b55',
	'#44bfea': '#2b85ae',
	'#61e296': '#3da567',
	'#da65ef': '#c93fda',
	'#f4e067': '#cdb942',
	'#282828': '#7b7b7b',
}

function changeHaikuColor() {
	var mainColor = $(this).parent().data('color');
	console.log(mainColor);
	var accentColor = accentColors[mainColor];
	$('body').css('background', mainColor);
	$('.color-box').css('background', mainColor);
	$('input').css('background', accentColor);
	$('.button').css('background', mainColor);
	$('.button').css('color', 'white');
};



$(document).ready(function(e) {
	// Show/hide comment section
	$('.comment-icon').on('click', function(e) {
  		$(this).parent().siblings('.comment-box').toggleClass('hide');
	});

	// Submit comment form
	$('.comment-form').on('submit', submitComment);

	// Edit comment
	$('.comment-list').on('click', '.comment-edit', displayEditComment);

	// Delete comment
	$('.comment-list').on('click', '.comment-delete', deleteComment);

	// Post upvote/downvote
	$('.vote-icon').on('click', upvoteDownvote);
	
	// Haiku color choice
	$('input[name="haiku-color"]:checked').each(changeHaikuColor);
	$('input[name="haiku-color"]').click(changeHaikuColor);
});

