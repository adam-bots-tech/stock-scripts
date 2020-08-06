import praw
import configuration
import re
import matplotlib.pyplot as plt

def get_hot_submissions():
	reddit = praw.Reddit(client_id=configuration.REDDIT_CLIENT_ID, client_secret=configuration.REDDIT_CLIENT_SECRET, user_agent=configuration.REDDIT_USER_AGENT)
	return reddit.subreddit("wallstreetbets").hot(limit=100);

def process_submissions(submissions, ticker, name, options_chart_path, karma_chart_path) :
	wsb_scores=[]
	wsb_labels=[]
	wsb_calls=0
	wsb_puts=0
	rendered_submissions = []

	for submission in submissions:

		if submission.title.find(ticker) < 0 and submission.title.find(name) < 0:
			continue

		rendered_submission = {}
		rendered_submission['title'] = submission.title
		rendered_submission['link'] = submission.url
		rendered_submissions.append(rendered_submission)

		wsb_calls += submission.selftext.count('call')
		wsb_puts += submission.selftext.count('put')
		wsb_calls += submission.title.count('call')
		wsb_puts += submission.title.count('put')

		call_refs = re.findall(r'\$\d+c', submission.selftext)
		if len(call_refs) > 0:
			wsb_calls += len(call_refs)
		put_refs = re.findall(r'\$\d+p', submission.selftext)
		if len(put_refs) > 0:
			wsb_puts += len(put_refs)

		call_refs = re.findall(r'\$\d+c', submission.title)
		if len(call_refs) > 0:
			wsb_calls += len(call_refs)
		put_refs = re.findall(r'\$\d+p', submission.title)
		if len(put_refs) > 0:
			wsb_puts += len(put_refs)

		#Aggregate the karma score by flair text
		score_index = 0
		try:
			score_index = wsb_labels.index(submission.link_flair_text)
		except ValueError:
			wsb_labels.append(submission.link_flair_text)
			score_index = wsb_labels.index(submission.link_flair_text)
		
		try:
			wsb_scores[score_index] += submission.score
		except IndexError:	
			wsb_scores.append(submission.score)

	plt.style.use('ggplot')
	plt.bar([i for i, _ in enumerate(wsb_scores)], wsb_scores, color='blue')
	plt.xlabel("Submission Flair")
	plt.ylabel("Karma Score")
	plt.title("WSB Submissions By Karma Score and Flair")
	plt.xticks([i for i, _ in enumerate(wsb_labels)], wsb_labels)
	# Write the barchart as a PNG to the data folder.
	plt.savefig(karma_chart_path)
	plt.close()

	plt.bar([i for i, _ in enumerate([wsb_calls, wsb_puts])], [wsb_calls, wsb_puts], color=['green', 'red'])
	plt.ylabel("Count")
	plt.title("WSB Calls and Puts References")
	plt.xticks([i for i, _ in enumerate(['Calls', 'Puts'])], ['Calls', 'Puts'])
	# Write the barchart as a PNG to the data folder.
	plt.savefig(options_chart_path)
	plt.close()

	return rendered_submissions