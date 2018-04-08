import sys
import argparse 
sys.path.append("..")
import spotipy
import spotipy.util as util
import json
import os.path
from time import sleep
from GoogleImageScrapper.google_images_download import google_images_download

scope = 'user-library-read'

username='aditya@clubastra.com'
token = util.prompt_for_user_token(username,scope,client_id='f0e821aa41b5409281e7f3cf2fcbf830',client_secret='a88d69473f504fe7a023a6717616f640',redirect_uri='http://localhost/')
flag=0
def GenerateArtistList():
	if(os.path.exists("./bandnames.txt")):
				GetImagesFromGoogle()
	else:
		if token:
			sp = spotipy.Spotify(auth=token)
			uri = 'spotify:user:12164215380:playlist:14okcYoZ5eK5KeNeHQYbuP'
			username = uri.split(':')[2]
			playlist_id = uri.split(':')[4]
			BandNames=list()
			results = sp.user_playlist(username, playlist_id)
			length= len(json.dumps(results['tracks']['items'][0]['track']))
			for x in range(0, length-1):
				try:
					temp=json.dumps(results['tracks']['items'][x]['track']['album']['artists'][0]['name'])
					temp=temp.replace('"','').replace("\\","")
					if temp not in BandNames:
						BandNames.append(temp)
				except IndexError:
					pass	
			if BandNames:
				file=open('bandnames.txt','w')
				for item in BandNames:
					file.write("%s\n" %item)
				print('file successfully created!')
				file.close()
				flag=1
			else:
				print('List is empty')


		else:
			print ("Can't get token for", username)


def GetImagesFromGoogle():
	response = google_images_download.googleimagesdownload()
	arguments = {"keywords_from_file":"bandnames.txt","limit":1,"size":"large"}

	response.download(arguments)
	


if __name__== "__main__":
	GenerateArtistList()
	if flag == 1:
		GenerateArtistList()