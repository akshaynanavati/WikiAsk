__version__ = "2.1"
import MontyTokenizer, MontyTagger, MontyLemmatiser, MontyREChunker, MontyExtractor, MontyNLGenerator

class MontyLingua:
    
    def __init__(self,trace_p=0):
        print '\n****** MontyLingua v.'+__version__+' ******'
        self.trace_p = trace_p
        self.theMontyTokenizer = MontyTokenizer.MontyTokenizer()
        self.theMontyLemmatiser = MontyLemmatiser.MontyLemmatiser()
        self.theMontyTagger = MontyTagger.MontyTagger(trace_p,self.theMontyLemmatiser)
        self.theMontyChunker = MontyREChunker.MontyREChunker()
        self.theMontyExtractor = MontyExtractor.MontyExtractor()
        self.theMontyNLGenerator = MontyNLGenerator.MontyNLGenerator()
        print '*********************************\n'

#
#  MAIN FUNCTIONS
#
    def generate_summary(self,vsoos):
        """
        uses MontyNLGenerator to generate a paragraph text summary
        in the past tense
        inputs a flat list of verb-subject-object-object tuples
      """
        return self.theMontyNLGenerator.generate_summary(vsoos)
            
    def generate_sentence(self,vsoo,sentence_type='declaration',tense='past',s_dtnum=('',1),o1_dtnum=('',1),o2_dtnum=('',1),o3_dtnum=('',1)):
        """
        inputs verb-subject-object-object tuple
        outputs a generated sentence
        
        valid sentence types: declarative, imperative, (can|may|would|should|could), (who|what|when|where|why|how), question
        valid tenses: past, present, progressive, past_progressive, future, infinitive
        dtnum is a pair of determiner, number e.g. ('the',1),('some',2)
        valid determiners = 'a','the','some','',etc
        valid numbers = 1,2,3
      """
        return self.theMontyNLGenerator.generate_sentence(vsoo,sentence_type=sentence_type,tense=tense,s_dtnum=s_dtnum,o1_dtnum=o1_dtnum,o2_dtnum=o2_dtnum,o3_dtnum=o3_dtnum)
        
    def jist_predicates(self,text):
	"""
        similar to jist() except output is simpler
        returns a list (document-level)
        of lists (sentence-level) of 
        lisp-style predicate argument structures
        - each structure should look something like this:
           - ("verb" "subject" "obj1" "obj2" ... )
        - words are all lemmatised, and determiners and
          modals are stripped out
        - obj's can be direct or indirect, but not
          subordinate clauses for now.
	"""	
        infos = self.jist(text)
        svoos_list = []
        for info in infos:
            svoos = info['verb_arg_structures_concise']
            svoos_list.append(svoos)
        return svoos_list
    
    def jist(self,text):
	"""
	inputs raw text, outputs a list of 
	dictionaries with information digests of 
	each sentence
	"""
        sentences = self.split_sentences(text)
        tokenized = map(self.tokenize,sentences)
        tagged = map(self.tag_tokenized,tokenized)
        chunked = map(self.chunk_tagged,tagged)
        #print "CHUNKED: " + string.join(chunked,'\n         ')
        extracted = map(self.extract_info,chunked)
        return extracted

    def pp_info(self,extracted_infos):
    	"""pretty prints sentence information digests returned by jist()"""
        for i in range(len(extracted_infos)):
            keys = extracted_infos[i].keys()
            keys.sort()
            print "\n\n   SENTENCE #%s DIGEST:\n"%str(i+1)
            for key in keys:
                print (key+": ").rjust(22) + str(extracted_infos[i][key])
    
    def split_paragraphs(self,text):
    	"""inputs a raw text and outputs a list of paragraph segments"""
        return self.theMontyTokenizer.split_paragraphs(text)

    def split_sentences(self,text):
	"""input a raw text and outputs a list of sentence segments"""
        return self.theMontyTokenizer.split_sentences(text)

    def tokenize(self,sentence,expand_contractions_p=1):
	"""
	inputs a raw text sentence and outputs that sentence 
	with punctuation tokenized, except in the case of abbreviations
    	iff expand_contractions_p == 1, then contractions will be
    	resolved (e.g. "can't"-->"can not")
    	"""
        return self.theMontyTokenizer.tokenize(sentence,expand_contractions_p)

    def tag_tokenized(self,tokenized_text):
	"""
	takes tokenized text and returns Penn Treebank tagset tagged text:
	i.e.:  "This/DT is/VB a/DT sentence/NN". 
	more information on the tagset can be found at:
	http://www.cis.upenn.edu/~treebank/
	"""
        return self.theMontyTagger.tag_tokenized(tokenized_text)

    def strip_tags(self,tagged_or_chunked_text):
    	"""
    	strips part-of-speech and chunk tags from text
    	and returns plaintext
    	"""
        toks = tagged_or_chunked_text.split()
        toks = filter(lambda x:'/' in x,toks)
        toks = map(lambda x:x.split('/')[0],toks)
        return ' '.join(toks)

    def parse_pred_arg(self,pp):
        """
        parses the predicate-argument string
        returned by jist_predicates(), of the form:
        '("pred name" "arg 1" "arg 2" etc)'
        and returns them as a list
        """
        # unpp augmented predicate
        pp.strip
        toks = pp.strip()[1:-1].split()
        args = ' '.join(toks)[1:-1].split('" "')
        return args
    
    def chunk_tagged(self,tagged_text):
    	"""
	chunks tagged text and outputs the form:
    	"(NX He/PRP NX) (VX is/VB VX) (NX the/DT mailman/NN NX)"    	
        """
        return self.theMontyChunker.Process(tagged_text)
    
    def chunk_lemmatised(self,lemmatised_text):
        """ 
        inputs lemmatised text of the form:
        "He/PRP/he ran/VBD/run"
        and outputs the form:
        "(NX He/PRP/he NX) (VX is/VB/be VX) (NX the/DT/the mailman/NN/mailman NX)"    	
       	"""
        return self.theMontyChunker.chunk_multitag(lemmatised_text)

    def lemmatise_tagged(self,tagged_text):
	"""
	lemmatises tagged text and outputs the form:
    	'These/DT/These sentences/NNS/sentence were/VBZ/be false/JJ/false'
    	(lemma follows the pos tag)
    	"""
        return self.theMontyLemmatiser.lemmatise_tagged_sentence(tagged_text)

                                   
    def extract_info(self,chunked_text):
    	"""
    	extracts many useful things from chunked_text
    	outputted in a dictionary, which can be printed using pp_info()
    	its keys and sample values:
    	noun_phrases: ['the dog','the cat']
    	noun_phrases_tagged: ['the/DT dog/NN','the/DT cat/NN']
        verb_phrases: ['will go quickly','go slowly']
        verb_phrases_tagged: ['will/MD go/VB quickly/RB','go/VB slowly/RB']
        prep_phrases: ['by the road','by chance']
        prep_phrases_tagged: ['by/IN the/DT road/NN','by/IN chance/NN']
        modifiers: ['red','best','quickly']
        modifiers_tagged: ['red/JJ','best/JJS','quickly/RB']
        verb_arg_structures: ['will/MD go/VB quickly/RB','the/DT dog/NN','to/IN the/DT cats/NNS']
        verb_arg_structures_concise: ['("go" "dog" "to cat")]
    	"""
    	return self.theMontyExtractor.extract_info(chunked_text,self.theMontyLemmatiser.lemmatise_tagged_sentence)
    
    
# END MONTYLINGUA CLASS

#        
# COMMAND LINE PROGRAM        
#
if __name__ == "__main__":
    import sys,time
    if '/?' in sys.argv or '-?' in sys.argv:
        print """
        USAGE: >> python MontyLingua.py 
        """
        sys.exit(0)


    m = MontyLingua()

 
    # show command prompt interface
    print '\n'

    try:
        while 1:
            sentence = ''
            try:
                sentence = raw_input('> ')
            except:
                raise

            time1 = time.time()
            print '\n'
            extractions = m.jist(sentence)                          
            #print m.pp_info(extractions)
            predicates_list = map(lambda a:m.parse_pred_arg(a),reduce(lambda y,z:y+z,map(lambda x:x['verb_arg_structures_concise'],extractions)))
            print predicates_list                           
            #print '\nGENERATED SUMMARY:\n'+m.generate_summary(predicates_list)
                
            time2= time.time()
            print "-- monty took",str(round(time2-time1,2)),'seconds. --\n'
    except KeyboardInterrupt:
        print "\n-- monty says goodbye! --"
        sys.exit(0)
       
