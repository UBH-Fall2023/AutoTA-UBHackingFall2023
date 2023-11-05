# AutoTA chatbot: the TA that always responds after 12 A.M!

## What is the core functionality of the chatbot?
Allows users to engage, via standard text, with a chatbot interface that will API with Open AI's ChatGPT 4.0 model. After receiving the data from their server(s), the response will be tuned to provide a TA-like response; this response aligns with academic integrity, as it does not provide explicit code nor replace the entire thinking process for a student. A primary feature is for it to draw a substantial part of its answer from course material, such as lecture slides, to provide a response, as well as a citation on the right side. 
## What technologies were used?
We used several languages: Python, Javascript, and CSS. On top of this, we used Django to streamline the process of connecting the front-end interface of the application with the back-end API and fine-tuning it- in a language we were all familiar with. We also used Bootstrap to streamline the CSS.

## Here are some examples:

You:
How to I dynamically allocate a string in C?
AutoTA:
To dynamically allocate a string in C, you should familiarize yourself with the process of dynamic memory allocation. This includes understanding the concept of the heap in memory, the structure of an array in C, and how to use functions such as malloc() or calloc() which can request a specific size of memory at runtime from the heap. Based on your desired length for the string, you'll have to allocate the proper amount of memory. Could you explain how you might calculate the size of memory you need to allocate for a string?

You:
Is it better to use malloc or calloc?
AutoTA:
The choice between malloc() and calloc() depends on your specific needs. If you're creating an array or data structure and you need every byte to be initialized to zero, then calloc() would be more efficient since it automatically zeroes out the memory that it allocates. On the other hand, malloc() will give you a block of memory without initializing it which could be a bit faster if you're planning on immediately writing over the memory and don't need it zeroed out. In terms of memory allocation size, when using both of these functions, how do you think you could calculate the amount of memory you would need to allocate?

You:
What about realloc?
AutoTA:
The function realloc() is used in C when you need to change the size of your already allocated memory. For instance, when you initially allocate memory for a certain number of elements and then later realize you need more or less space, you can use realloc() to adjust the allocation accordingly. The way realloc works is that it tries to increase the size of the memory block that was previously allocated. If it can't, it allocates a new block of memory, copies over the old data, and then frees the old block. Do you comprehend why you might need to use realloc() and how you would use it in your code?

-------------------------------

 ![first image](/firstImage.png)

 ![secondimage](/secondIMgae.png)


