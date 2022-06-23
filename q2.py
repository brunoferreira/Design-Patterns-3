from abc import abstractmethod

class User():
    """
    User class
    """
    def __init__(self, isAdmin, isAuthor):
        self.isAdmin = isAdmin
        self.isAuthor = isAuthor


class Document():
    """
    Dcoument class
    """
    def __init__(self):
        self.state = None
        self.user = None

    def render(self):
        self.state.render()

    def publish(self):
        self.state.publish()
    
    def change_state(self, state):
        self.state = state

class State():
    """
    State abstract class
    """
    def __init__(self, document):
        self.document = document

    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def publish(self):
        pass
    

class Draft(State):
    """
    Draft class (inherits from State abstract class)
    """
    def render(self):
        if self.document.user.isAdmin or self.document.user.isAuthor:
            print(self)
        else:
            print('No admin or author')

    def publish(self):
        if self.document.user.isAdmin:
            published_state = Published(self.document)
            self.document.change_state(published_state)
        else:
            moderation_state = Moderation(self.document)
            self.document.change_state(moderation_state)

class Moderation(State):
    """
    Moderation class (inherits from State abstract class)
    """
    def render(self):
        if self.document.user.isAdmin or self.document.user.isAuthor:
            print(self)
        else:
            print('No admin or author')

    def publish(self):
        if self.document.user.isAdmin:
            published_state = Published(self.document)
            self.document.change_state(published_state)
        else:
            print('Review Failed')
            draft_state = Draft(self.document)
            self.document.change_state(draft_state)


class Published(State):
    """
    Published class (inherits from State abstract class)
    """
    def render(self):
        if self.document.user.isAdmin or self.document.user.isAuthor:
            print(self)
        else:
            print('No admin or author')

    def publish(self):
        print("Already published. State remains the same.")


def run():
    """
    Simple test
    """
    user = User(isAdmin=True, isAuthor=False)
    doc = Document()
    doc.user = user
    draft_state = Draft(doc)
    doc.change_state(draft_state)
   
    print(doc.state)
    doc.publish()
    print(doc.state)
    doc.publish()
    print(doc.state)


if __name__ == "__main__":
    run()