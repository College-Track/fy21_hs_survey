import ezgmail

ezgmail.init()


emails = [
    {"site": "Oakland", "sd": "Miccaela", "email": "mmontague@collegetrack.org"},
    {"site": "Boyle Heights", "sd": "Tina", "email": "tkim@collegetrack.org"},
    {"site": "Sacramento", "sd": "Luisana", "email": "lvictorica@collegetrack.org"},
    {"site": "New Orleans", "sd": "Clara", "email": "cbaron@collegetrack.org"},
    {"site": "Watts", "sd": "John", "email": "johnlee@collegetrack.org"},
    {"site": "Aurora", "sd": "Dan", "email": "dsullivan@collegetrack.org"},
    {"site": "Crenshaw", "sd": "Wintor", "email": "wmcneel@collegetrack.org"},
    {"site": "Denver", "sd": "Cole", "email": "njimenez@collegetrack.org"},
    {"site": "San Francisco", "sd": "KD", "email": "kdevinna@collegetrack.org"},
    {"site": "East Palo Alto", "sd": "June", "email": "jafshar@collegetrack.org"},
    {"site": "Ward 8", "sd": "Barry", "email": "bbrinkley@collegetrack.org"},
    {"site": "The Durant Center", "sd": "Jane", "email": "jharris@collegetrack.org"},
]

message = """
Hi {sd},<br><br>

Thank you for the hard work in getting all the student survey data in!<br><br>

This year we asked students if they were comfortable sharing their responses with CT staff at their site. For the student who accepted this, we generated an excel file with all of their responses for you to look over. That data is attached here in the first tab of the excel file. Feel free to share this among your site as you feel is appropriate<br><br>

In addition, I wanted to share with you the results of some analysis we did for each site. The second and third tabs of the attached file list any question that a group of students at your site responded notably above or below the College Track average.<br><br>

The first tab list all the questions, and group of students, who responded more favorably than the College Track average, while the second tab list all the questions and groups of students who responded less positively than the CT average.<br><br>

We only recognized a group of students as being notable if they were above or below the CT average by 10% and if the group of students contained at least 25 students. This was done to ensure the sample sizes were sufficient to draw conclusions.<br><br>

Let me know if you have any questions about this, but hopefully it helps you understand your survey results in a more meaningful way! <br><br>

As a reminder, you can find the HS Survey Executive Summary <a href="https://datapane.com/u/baker/reports/fy21-hs-survey-executive-summary/">here</a> and the Data Studio dashboard <a href="https://datastudio.google.com/reporting/8ec5c940-2f56-4abc-a37f-39217609ce4f">here</a>.<br><br>

Thanks,
<br>
Baker
"""

for site in emails:
    file = "data/processed/individual_responses/{}_individual_responses.xlsx".format(
        site["site"]
    )
    ezgmail.send(
        site["email"],
        # "brenneckar@collegetrack.org",
        "[Update] Additional HS Survey Data for {}".format(site["site"]),
        message.format(sd=site["sd"]),
        attachments=[file],
        cc="vshah@collegetrack.org",
        mimeSubtype="html",
    )

