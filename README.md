# Secret Santa Generator

Very basic command-line tool to generate giver-receiver pairs from a list of partecipants. The associations are done via numpy.random.shuffle function. If a partecipant is mapped to itself, try again. For small groups this approach is acceptable, for larger ones I have not tried directly, but it is not so efficient; let me try to elaborate.

Given $N$ ordered integers, there are $N!$ permutations without repetitions. What is fraction of these permutation in which no element is left at its original position, i.e. there are not fixed points? Turns out it's the _subfactoria_ $!N$, and what we are trying to do is a derangement [https://en.wikipedia.org/wiki/Derangement]. What is important for us is that the ratio between the permutation without fix point and all possible permutations quickly converges $\lim_{N\to \infty} !N/N! \to 1/e \approx 0.37$. 

So, a little more thana a third of our permuations will satifsy our not-fixed-point requirment. This means that after three shuffles we should get a valid one. If we have about 10 elements, each shuffle take a fraction of a second, so this approach is acceptable. For billions of elements to shuffle (a World Wide Secred Santa!), the action of shufflinig is far more expensive and this approach is not viable anymore and you will have to scratch you head to find a better solution.


### Input
The script takes the input as a json, like the example one in the repository:
```
{
    "partecipants": {
        "Alice": "alice@gmail.com",
        "Bob": "bob@outlook.com",
        "John Doe": "john@live.com",
        "Jane Doe": "jane@what.ever"
    }
}
```

There *must* be an element called ```partecipants``` wich is a dictionary of entries ```name: email_address```.
Optionally you can specify a ```budget``` field.

### Emailing
All the email will come from a *gmail* address (just because the server details are hard-coded). The script will ask you for the address and password. For this to work, you need to have the 2-step verification on and generate (and use here) a AppPassword (see google account -> security).


### To implement
- you might want to have exclusion clauses, e.g. be sure you don't have to buy a gift for that cousine you don't like. This should be just another check on the shuffle. I'm just a bit lazy.
