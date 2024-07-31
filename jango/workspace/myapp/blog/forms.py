from django import forms
from .models import Post,Category

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)

class PostForm(forms.Form):        
       
        title=forms.CharField(
              label='Title',
              widget=forms.TextInput(attrs={'class':'form-control'}),
              error_messages={
                    'required':'Title is required',
              }
              )
        category=forms.CharField(
              label='Category',
            #   widget=forms.TextInput(attrs={'class':'form-control'})
              error_messages={
                    'required':'Category is required',
                    }
                    )
        content=forms.CharField(
              label='Content',
              widget=forms.Textarea(attrs={'class':'form-control', 'rows':3}),
              error_messages={
                    'required':'Content is required',
                    }
                    )
        img_url=forms.CharField(
              label='Image URL',max_length=100,
              widget=forms.TextInput(attrs={'class':'form-control'}),
              error_messages={
                    'required':'Image URL is required',
                    }
                    )
        
        class Meta:
              model = Post
              fields = '__all__'
        
        def __init__(self, *args, **kwargs):
                # Optionally pass the instance data to populate fields
                self.instance = kwargs.pop('instance', None)
                super().__init__(*args, **kwargs)
                if self.instance:
                    self.fields['title'].initial = self.instance.title
                    self.fields['category'].initial = self.instance.category_id
                    self.fields['content'].initial = self.instance.content
                    self.fields['img_url'].initial = self.instance.img_url

        def save(self):
                if self.instance:
                    # Update the instance with cleaned data
                    self.instance.title = self.cleaned_data['title']
                    self.instance.category_id = self.cleaned_data['category']
                    self.instance.content = self.cleaned_data['content']
                    self.instance.img_url = self.cleaned_data['img_url']
                    self.instance.save()
                return self.instance

      
      #   def save(self, commit=True):
      #       post = super().save(commit=False)
      #       post.slug = slugify(self.cleaned_data['title'])
      #       if commit:
      #             post.save()
      #       return post  
        