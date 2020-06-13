import discord
from discord.ext import commands


def update_list(assignment):
    assignments.append(assignment)
    with open("assignments.txt", "a") as file_object:
        file_object.write(assignment)

assignments = []
with open("assignments.txt") as file_object:
    lines = file_object.readlines()
    for line in lines:
        try:
            assignments.append(line.rstrip())
        except:
            print("Empty message")
                    
total = 0

class Submission(commands.Cog):
    """Its all commands relating to submissions. Submit your asssignment using .submit"""
    def __init__(self, client):
        self.client = client

    


    @commands.command(aliases=["Submission", "Add"])
    async def submit(self, ctx, link, *, assignment):
        """This function allows you to submit any assignments that are assigned to you"""
        global total
        for element in assignments:
            if(assignment == element):
                user = ctx.author
                name = user.display_name
                with open("submissions.txt", "a") as file_object:
                    file_object.write("{} posted the assignment {}: {}\n".format(name, assignment, link))
            else:
                total += 1
        if(total == len(assignments)):
            await ctx.send("Assignment ,{}, is not found. Please do the .show_a command to show all assignments.".format(assignment))
            
        
            

    @commands.command(aliases=["show_assign", "show_assignments", "show_a"])
    async def all_assignments(self, ctx):
        """This function allows you to see all assignments that the Admins have posted"""
        print(", ".join(assignments))
        await ctx.send(", ".join(assignments))

    @commands.command(aliases=["append_list", "add_list", "add_a"])
    @commands.has_any_role("Admin", "Moderator")
    async def add_to_assignments(self, ctx, *, assignment):
        """This function allows you to add an assignment to the list. Admins Only"""
        update_list(assignment)
        await ctx.send("{} has been sent".format(assignment))

    @commands.command(aliases=["show_submissions", "s"])
    @commands.has_any_role("Admin", "Moderator", "Tutor")
    async def show_sub(self, ctx):
        """This function allows you to show all submissions from students. Admins and Tutors only."""
        with open("submissions.txt") as file_object:
            lines = file_object.readlines()
            for line in lines:
                try:
                    await ctx.send(line)
                except:
                    print("Empty message")

def setup(client):
    client.add_cog(Submission(client))

