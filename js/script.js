// HELPERS

function getSelfUsername() {
	return $.trim($('#signedin-username').text());
}

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
	"		<img src='/assets/comments_close.png' class='comment-edit-button close-comment-edit'>" +
	"		<input type='submit' value='SUBMIT' class='comment-button'>" +
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
		.closest('.individual-comment-box');

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
		.closest('.individual-comment-box');
	var commentID = commentContainer
		.attr('data-commentid');
	var haikuID = commentEditSubmitInstance
		.closest('.comment-scroll-list-box')
		.siblings('.comment-add-box')
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
		.closest('.individual-comment-box')
		.attr('data-commentid');
	var haikuID = commentDeleteInstance
		.closest('.comment-scroll-list-box')
		.siblings('.comment-add-box')
		.attr('data-haikuid');

	var deleteCommentUrl = '/' + haikuID + '/comment/' + commentID + '/delete';
	var data = {
		'commentID': commentID
	}
	var votePost = $.post(deleteCommentUrl, data);
	votePost.done(function() {
		var commentCounter = commentDeleteInstance
			.closest('.comment-box-container')
			.siblings('.comment-header')
			.children('p');

		var commentCount = commentCounter.text()
		if (commentCount == 1) {
			commentCount = '';
		} else {
			commentCount = parseInt(commentCount) - 1;
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
	var haikuID = commentInstance
		.closest('.comment-add-box')
		.attr('data-haikuid');
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
			.find('.new-comment-text')
			.val('');
		var commentList = commentInstance
			.closest('.comment-list-box');
		commentPost.done(function() {
			var commentCounter = commentList
				.closest('.comment-box-container')
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
	var voteInstance = $(this);

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
	'#333333': '#7b7b7b',
}

function changeHaikuColor() {
	var mainColor = $(this).parent().data('color');
	console.log(mainColor);
	var accentColor = accentColors[mainColor];
	$('body').css('background', mainColor);
	$('.color-box').css('background', mainColor);
	$('.haiku-input').css('background', accentColor);
	$('.button').css('background', mainColor);
	$('.button').css('color', 'white');
};



$(document).ready(function(e) {
	// Comment scrollbar
	$('.comment-list-box').niceScroll({
		cursorcolor: '#ffffff',
		cursorwidth: '3px',
		cursorborder: '0px',
	});

	// Show/hide comment section
	$('.comment-icon').on('click', function(e) {
  		$(this)
  			.parent()
  			.siblings('.comment-box-container')
  			.toggleClass('hide');

  		$('.comment-list-box').getNiceScroll().resize();

  		var shownHeight = $(this)
  			.parent()
  			.siblings('.comment-box-container')
  			.find('.comment-list-box')
  			.height();
  		var contentHeight = $(this)
  			.parent()
  			.siblings('.comment-box-container')
  			.find('.comment-list-box')
  			.prop('scrollHeight');
  		console.log('shownHeight:', shownHeight)
  		console.log('contentHeight:', contentHeight)
  		if (contentHeight > shownHeight) {
  			$(this)
  				.parent()
  				.siblings('.comment-box-container')
  				.find('.comment-scroll-box')
  				.toggleClass('hide');
  		}
	});

	// Scroll content
	$('.scroll-up').click(function () {
    	$('.comment-list-box').scrollTop($('.comment-list-box').scrollTop() - 50);
	});

	$('.scroll-down').click(function () {
    	$('.comment-list-box').scrollTop($('.comment-list-box').scrollTop() + 50);
	});

	// Show/hide comment add
	$('.comment-add-icon').on('click', function() {
		console.log('clicked')
		$(this).parent().siblings('.comment-add').toggleClass('hide');
	})

	// Submit comment form
	$('.comment-form').on('submit', submitComment);

	// Edit comment
	$('.comment-list-box').on('click', '.comment-edit', displayEditComment);

	// Delete comment
	$('.comment-list-box').on('click', '.comment-delete', deleteComment);

	// Post upvote/downvote
	$('.vote-icon').on('click', upvoteDownvote);
	
	// Haiku color choice
	$('input[name="haiku-color"]:checked').each(changeHaikuColor);
	$('input[name="haiku-color"]').click(changeHaikuColor);
});

