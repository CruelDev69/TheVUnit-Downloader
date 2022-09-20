'''
MIT License

Copyright (c) 2022 Ahad 

If you want to use this code for any purpose, kindly give credits before using. 
You can modify or edit it but you are not allowed to remove the author name 
from the code.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from pytube import YouTube # Importing YouTube class from module pytube.
from colorama import Fore # Importing colorama

print(Fore.RED + '''
╦ ╦┌─┐┬ ┬╔╦╗┬ ┬┌┐ ┌─┐  ╦  ╦┬┌┬┐┌─┐┌─┐  ╔╦╗┌─┐┬ ┬┌┐┌┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
╚╦╝│ ││ │ ║ │ │├┴┐├┤   ╚╗╔╝│ ││├┤ │ │   ║║│ ││││││││  │ │├─┤ ││├┤ ├┬┘
 ╩ └─┘└─┘ ╩ └─┘└─┘└─┘   ╚╝ ┴─┴┘└─┘└─┘  ═╩╝└─┘└┴┘┘└┘┴─┘└─┘┴ ┴─┴┘└─┘┴└─
'''+ Fore.RESET)
print(Fore.YELLOW +'''
Author: Ahad#3257                            
Website: https://itscruel.cf
Github: https://github.com/CruelDev69/YouTube-Video-Downloader
'''+ Fore.RESET)

Link = str(input(Fore.BLUE + "Enter URL of a YouTube Video to download: " + Fore.RESET)) # Requiring Link of YouTube video from user.
yt = YouTube(Link) # Giving link to class.
print(f"{Fore.GREEN}[MESSAGE]: Wait while tool downloads the video it can take several minutes depends on your internet.{Fore.RESET}")
yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download() # Downloading video in mp4 format.