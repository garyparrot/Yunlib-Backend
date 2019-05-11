from linebot.models import *

footer_style = { "separator": True }
main_title_style = { 
        "weight": "bold",
        "color": "#1DB446",
        "size": "md" 
        }
section_title_box_style = {
        "layout": "horizontal"
        }
section_title_style = {
        "weight": "bold",
        "margin": "sm",
        "size": "xxl",
        "flex": 7
        }
section_subtitle_style = {
        "wrap": True,
        "color": "#aaaaaa",
        "size": "xs",
        "align": "end",
        "gravity": "bottom",
        "flex": 3
        }
section_booklist_style = { 
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm"
        }
section_bookrow_style = {
        "layout": "horizontal"
        }
section_bookname_style = {
        "flex": 7,
        "size": "sm",
        "color": "#555555",
        }
section_duedate_style = {
        "flex": 3,
        "size": "sm",
        "color": "#111111",
        "align": "end"
        }
section_duedate_urgent_style = {
        "flex": 3,
        "size": "sm",
        "color": "#ee3333",
        "align": "end"
        }
footer_box_style = {
        "layout": "horizontal",
        "margin": "md",
        }
footer_left_style = {
        "size": "xs",
        "color": "#aaaaaa",
        "flex": 0
        }
footer_right_style = {
        "size": "xs",
        "color": "#aaaaaa",
        "align": "end"
        }
separator_style = {
        "margin": "md"
        }

class BookStatRender:

    def __init__(self, statistic_data):
        self.data = statistic_data

    def Render(self):
        return self.RenderBookStat()

    def RenderBookStat(self):
        return BubbleContainer(
                body   = self.RenderBody(),
                footer = self.RenderFooter(self.data['footer']),
                styles = BubbleStyle(footer=BlockStyle(**footer_style))
                )

    def RenderBody(self):
        contents = [self.RenderTitle(self.data)]

        for section in self.data['contents']:
            contents.append(self.RenderSection(section))

        return BoxComponent(contents = contents, layout="vertical")

    def RenderTitle(self, data):
        return TextComponent(text=data["main_title"],**main_title_style )

    def RenderSection(self, data):
        contents = [self.RenderSectionTitle(data), self.RenderSeparator()]

        for book in data['booklist']:
            contents.append(self.RenderBook(book)) 

        return BoxComponent(contents = contents, **section_booklist_style)

    def RenderSectionTitle(self, data):
        section_title = TextComponent(text=data['section_title'], **section_title_style)
        section_subtitle = TextComponent(text=data['section_subtitle'], **section_subtitle_style)
        
        return BoxComponent(contents = [section_title, section_subtitle], **section_title_box_style)

    def RenderBook(self, book):
        Tbook = TextComponent(text=book['bookname'], **section_bookname_style) 
        if book.get('urgent',False) == True:
            Tduedate = TextComponent(text=book['duedate'], **section_duedate_urgent_style)
        else:
            Tduedate = TextComponent(text=book['duedate'], **section_duedate_style)

        return BoxComponent(contents = [Tbook,Tduedate], **section_bookrow_style)

    def RenderSeparator(self):
        return SeparatorComponent(**separator_style)

    def RenderFooter(self, footer):
        footer_left = self.RenderLeft(footer['left'])
        footer_right = self.RenderRight(footer['right'])

        return BoxComponent(contents = [footer_left, footer_right], **footer_box_style)

    def RenderLeft(self, left):
        return TextComponent(text=left, **footer_left_style)

    def RenderRight(self,right):
        return TextComponent(text=right, **footer_right_style)
