"""
1.This Software copyright \u00A9 Australian Synchrotron Research Program Inc, ("ASRP").

2.Subject to ensuring that this copyright notice and licence terms
appear on all copies and all modified versions, of PyCIFRW computer
code ("this Software"), a royalty-free non-exclusive licence is hereby
given (i) to use, copy and modify this Software including the use of
reasonable portions of it in other software and (ii) to publish,
bundle and otherwise re-distribute this Software or modified versions
of this Software to third parties, provided that this copyright notice
and terms are clearly shown as applying to all parts of software
derived from this Software on each occasion it is published, bundled
or re-distributed.  You are encouraged to communicate useful
modifications to ASRP for inclusion for future versions.

3.No part of this Software may be sold as a standalone package.

4.If any part of this Software is bundled with Software that is sold,
a free copy of the relevant version of this Software must be made
available through the same distribution channel (be that web server,
tape, CD or otherwise).

5.It is a term of exercise of any of the above royalty free licence
rights that ASRP gives no warranty, undertaking or representation
whatsoever whether express or implied by statute, common law, custom
or otherwise, in respect of this Software or any part of it.  Without
limiting the generality of the preceding sentence, ASRP will not be
liable for any injury, loss or damage (including consequential loss or
damage) or other loss, loss of profits, costs, charges or expenses
however caused which may be suffered, incurred or arise directly or
indirectly in respect of this Software.

6. This Software is not licenced for use in medical applications.
"""

from types import *
import re
class BlockCollection:
    def __init__(self,datasource=None,strict=1,type_tag=''):
        self.dictionary = {}
        self.type_tag = type_tag
        self.strict = strict
        self.lower_keys = []              # for efficiency
        if isinstance(datasource,DictType):
            for (key,value) in datasource.items():
                self.__setitem__(key,value)
        elif isinstance(datasource,CifFile) or isinstance(datasource,BlockCollection):
            for key,value in datasource.dictionary.items():
                self.dictionary[key] = value.copy()     # a deep copy
            self.lower_keys = map(lambda a:a.lower(),self.dictionary.keys()) 
        if strict:
            self.checklengths()
        self.header_comment = ''

    def checklengths(self):
        toolong = filter(lambda a:len(a)>75, self.dictionary.keys())
        if toolong:
            errorstring = ""
            for bn in toolong:
                errorstring += "\n" + bn
            raise CifError, 'Following block name(s) too long: \n' + errorstring

    def __str__(self):
        return self.WriteOut()

    def __setitem__(self,key,value):
        if isinstance(value,CifBlock):
            self.NewBlock(key,value,replace=True)
        elif isinstance(value,DictType):
            self.NewBlock(key,CifBlock(value),replace=True)
        else: raise TypeError
        self.lower_keys.append(key.lower())

    # due to attempt to get upper/lower case treated as identical
    # we have a bit of cruft here
    def __getitem__(self,key):
        try:
            return self.dictionary[key]
        except KeyError:
            if key.lower() not in self.lower_keys:
                raise KeyError
        curr_keys = self.dictionary.keys()
        lower_ordered = map(lambda a:a.lower(),curr_keys)
        keyindex = lower_ordered.index(key.lower())
        return self.dictionary[curr_keys[keyindex]]

    # we have to get an ordered list of the current keys,
    # as we'll have to delete one of them anyway
    def __delitem__(self,key):
        try:
            del self.dictionary[key]
            self.lower_keys.remove(key.lower())
        except KeyError:
            if not self.has_key(key):
                raise KeyError
            curr_keys = self.dictionary.keys()
            lower_ordered = map(lambda a:a.lower(),curr_keys)
            keyindex = lower_ordered.index(key.lower())
            del self.dictionary[curr_keys[keyindex]]
        
    def __len__(self):
        return len(self.dictionary)

    def keys(self):
        return self.dictionary.keys()

    # changes to take case independence into account
    def has_key(self,key):
        if self.dictionary.has_key(key):
           return 1
        if key.lower() in self.lower_keys:
           return 1
        return 0

    def get(self,key,default=None):
        if self.dictionary.has_key(key):
            return self.dictionary[key]
        elif self.has_key(key):     # take account of case
            return self.__getitem__(key)
        else:
            return default

    def clear(self):
        self.dictionary.clear()
        self.lower_keys = []

    def copy(self):   
        newcopy = self.dictionary.copy()
        return BlockCollection('',newcopy)
     
    def update(self,adict):
        for key in adict.keys():
            self.dictionary[key] = adict[key]
        self.lower_keys.extend(map(lambda a:a.lower(),adict.keys()))

    def items(self):
        return self.dictionary.items()

    def ReadCif(self,filestream,strict=1,maxlength=2048):
        import YappsCifParser,string
        text = filestream.read()
        if not text:      # empty file, return empty block
            return
        split = string.split(text,'\n')
        if strict:
            toolong =  filter(lambda a:len(a)>maxlength, split)
            if toolong:
                pos = split.index(toolong[0])
                raise CifError, 'Line %d contains more than %d characters' % (pos+1,maxlength)
        context = {"loops":[],"latest":{}}
        try: 
            parser = YappsCifParser.CifParser(YappsCifParser.CifParserScanner(text))
            filecontents = getattr(parser,"input")()
        except YappsCifParser.SyntaxError:
            errorstring = 'Syntax error in input file: last value parsed was %s' % YappsCifParser.lastval
            errorstring = errorstring + '\nParser status: %s' % `parser._scanner`
            raise CifError, errorstring
        else:
            if not filecontents: # comments only, return empty
                return
        for block in filecontents.keys():
            # check for looped-unlooped name collisions
            thisblock = filecontents[block]
            if len(thisblock["loops"])>0 :        #for efficiency
               unloop_keys = thisblock.keys()
               unloop_lower_keys = map(lambda a:a.lower(),unloop_keys)
               loop_keys = []
               for loop in thisblock["loops"]:
                  loop_keys.extend(loop.keys())
               #print "ReadCif: comparing %s to %s" % (`unloop_keys`,`loop_keys`)
               bad = filter(lambda a:a.lower() in unloop_lower_keys,loop_keys)
               if len(bad)>0:
                  errorstring  = "Following keys duplicated in block %s:" % block
                  for k in bad: errorstring += " %s" % k
                  raise CifError, errorstring 
            self.dictionary.update({block:CifBlock(filecontents[block])})

    def NewBlock(self,blockname,blockcontents=(),replace=False):
        if not blockcontents:
            blockcontents = CifBlock()
        newblockname = re.sub('[  \t]','_',blockname)
        new_lowerbn = newblockname.lower()
        if self.lower_keys.count(new_lowerbn):    #already in CIF
            if not replace:
                raise CifError, "Attempt to replace existing block" + blockname
            # generate a list of lower-case keys in correct order
            current_keys = self.dictionary.keys()
            blocknames = map(lambda a:a.lower(),current_keys)
            location = blocknames.index(new_lowerbn)
            del self.dictionary[current_keys[location]]
        if len(blockname) > 75:
            raise CifError, 'Cif block/frame name too long:' + blockname
        if blockcontents.__class__.__name__[-8:] != 'CifBlock':
            raise CifError, 'Cif block initialised with non CifBlock object %s' % blockcontents.__class__.__name__[-8:]
        self.dictionary.update({blockname:blockcontents})
        self.lower_keys.append(new_lowerbn)

    def merge(self,new_bc,mode="strict",single_block=[],
                   idblock="",match_att=""):
        if single_block:
            self.dictionary[single_block[0]].merge(new_bc[single_block[1]],mode,
                                                   match_att=match_att)
            return None
        base_keys = self.keys()
        block_to_item = base_keys   #default
        new_keys = new_bc.keys()
        if match_att:
            #make a blockname -> item name map
            block_to_item = map(lambda a:self[a].get(match_att,None),self.keys())
            # print `block_to_item`
        for key in new_keys:
            if key == idblock: continue
            basekey = key        #default value
            attval = new_bc[key].get(match_att,0)
            for ii in range(len(block_to_item)):  #do this way to get looped names
                thisatt = block_to_item[ii]
                #print "Looking for %s in %s" % (attval,thisatt)
                if attval == thisatt or \
                   (isinstance(thisatt,ListType) and attval in thisatt):
                      basekey = base_keys.pop(ii)
                      block_to_item.remove(thisatt)
                      break
            if not self.dictionary.has_key(basekey) or mode=="replace":
                self.dictionary[basekey] = new_bc[key]
            else:
                if mode=="strict":
                    raise CifError, "In strict merge mode: block %s in old and block %s in new files" % (basekey,key)
                elif mode=="overlay":
                    self.dictionary[basekey].merge(new_bc[key],mode,match_att=match_att)
                else:  
                    raise CifError, "Merge called with unknown mode %s" % mode

    def get_all(self,item_name):
        raw_values = map(lambda a:self[a].get(item_name),self.dictionary.keys())
        raw_values = filter(lambda a:a != None, raw_values)
        ret_vals = []
        for rv in raw_values:
            if isinstance(rv,ListType):
                for rvv in rv:
                    if rvv not in ret_vals: ret_vals.append(rvv)
            else:
                if rv not in ret_vals: ret_vals.append(rv)
        return ret_vals

    def WriteOut(self,comment=''):
        import cStringIO
        if not comment:
            comment = self.header_comment
        outstring = cStringIO.StringIO()
        outstring.write(comment)
        for datablock in self.dictionary.keys():
            outstring.write('\n' + self.type_tag +datablock+'\n')
            outstring.write(str(self.dictionary[datablock]))
        returnstring =  outstring.getvalue()
        outstring.close()
        return returnstring


class CifFile(BlockCollection):
    def __init__(self,datasource=None,strict=1,maxinlength=2048,maxoutlength=0):
        BlockCollection.__init__(self,datasource=datasource,strict=strict,type_tag='data_')
        self.maxinlength = maxinlength
        if maxoutlength == 0:
            self.maxoutlength = maxinlength
        else:
            self.maxoutlength = maxoutlength
        if type(datasource) is StringType:
            filestream = open(datasource)
            self.ReadCif(filestream,strict,maxinlength)
            filestream.close()
        self.header_comment = \
"""#\\#CIF1.1
##########################################################################
#               Crystallographic Information Format file 
#               Produced by PyCifRW module
# 
#  This is a CIF file.  CIF has been adopted by the International
#  Union of Crystallography as the standard for data archiving and 
#  transmission.
#
#  For information on this file format, follow the CIF links at
#  http://www.iucr.org
##########################################################################
"""

    def ReadCif(self,filestream,strict=1,maxlength=2048):
        import YappsCifParser,string
        text = filestream.read()
        # remove Ctrl-Z at end of file
        for i in xrange(len(text)-1,0,-1):
          c = text[i]
          if (c == '\x1a'):
            text = text[:i]
            break
          if (not c.isspace()):
            break
        if not text:      # empty file, return empty block
            return
        split = string.split(text,'\n')
        if strict:
            toolong =  filter(lambda a:len(a)>maxlength, split)
            if toolong:
                pos = split.index(toolong[0])
                raise CifError, 'Line %d contains more than %d characters' % (pos+1,maxlength)
        context = {"loops":[],"latest":{}}
        try: 
            parser = YappsCifParser.CifParser(YappsCifParser.CifParserScanner(text))
            filecontents = getattr(parser,"input")()
        except YappsCifParser.SyntaxError:
            errorstring = 'Syntax error in input file: last value parsed was %s' % YappsCifParser.lastval
            errorstring = errorstring + '\nParser status: %s' % `parser._scanner`
            raise CifError, errorstring
        else:
            if not filecontents: # comments only, return empty
                return
        for block in filecontents.keys():
            # check for looped-unlooped name collisions
            thisblock = filecontents[block]
            if len(thisblock["loops"])>0 :        #for efficiency
               unloop_keys = thisblock.keys()
               unloop_lower_keys = map(lambda a:a.lower(),unloop_keys)
               loop_keys = []
               for loop in thisblock["loops"]:
                  loop_keys.extend(loop.keys())
               #print "ReadCif: comparing %s to %s" % (`unloop_keys`,`loop_keys`)
               bad = filter(lambda a:a.lower() in unloop_lower_keys,loop_keys)
               if len(bad)>0:
                  errorstring  = "Following keys duplicated in block %s:" % block
                  for k in bad: errorstring += " %s" % k
                  raise CifError, errorstring 
            self.dictionary.update({block:CifBlock(filecontents[block])})


class CifBlock:
    def __init__(self,data = (), strict = 1, maxoutlength=2048,wraplength=80):
        self.block = {"loops":[],"saves":BlockCollection(type_tag="save_")}
        self.maxoutlength = maxoutlength
        self.wraplength = wraplength
        self.lower_keys = []    #for efficiency
        if type(data) is DictType:     #direct placement
            self.block.update(data)
            # convert any save frames to CifBlocks
            sbs = self.block["saves"]  #shorthand
            self.block["saves"] = BlockCollection(datasource=sbs,strict = strict, type_tag="save_")
        elif isinstance(data,(TupleType,ListType)):
            for item in data:
                self.AddCifItem(item)
        else:                          #assume is CifBlock
            self.block = data.block.copy()
        if strict:
            self.checklengths()
        # initialise our list of lower-case keys
        self.lower_keys = map(lambda a:a.lower(),self.keys())
        self.lower_keys.extend(["loops","saves"])

    def __str__(self):
        return self.printsection()

    def __setitem__(self,key,value):
        self.AddCifItem((key,value))

    def __getitem__(self,key):
        return self.GetCifItem(key)

    def __delitem__(self,key):
        self.RemoveCifItem(key)

    def __len__(self):
        blen = len(self.block) - 1   #non-looped items
        if self.block.has_key("saves"): blen = blen - 1  #not counted 
        for aloop in self.block["loops"]:
            blen = blen + len(aloop.keys())
        return blen    

    def __nonzero__(self):
        if self.__len__() > 0: return 1
        return 0

    # keys ignores the "saves" key
    def keys(self):
        thesekeys = self.block.keys()
        for aloop in self.block["loops"]:
            thesekeys.extend(aloop.keys())
        try:
            thesekeys.remove("saves")
            thesekeys.remove("loops")
        except ValueError:
            pass
        return thesekeys

    def values(self):
        ourkeys = self.keys()
        return map(lambda a:self[a],ourkeys)

    def has_key(self,key):
        if key.lower() in self.lower_keys:
            return 1
        return 0

    def get(self,key,default=None):
        if self.has_key(key):
            retval = self.GetCifItem(key)
        else:
            retval = default
        return retval

    def clear(self):
        self.block = {"loops":[],"saves":BlockCollection(type_tag="save_")}
        self.lower_keys = ["loops","saves"]

    def copy(self):
        newcopy = self.block.copy()
        newcopy["loops"] = []
        for aloop in self.block["loops"]:  # do a deeper copy
            newcopy["loops"].append(aloop.copy())
        if self.block.has_key("saves"):    # a block collection object
            newcopy["saves"] = self.block["saves"].copy()
        return CifBlock(newcopy)

    # this is not appropriate for save blocks.  Instead, the save block
    # should be accessed directly for update
     
    def update(self,adict):
        loopdone = []
        if not isinstance(adict,CifBlock):
            raise TypeError
        for key in adict.block.keys():
            if key!="loops":
                self.AddCifItem((key,adict[key]))
            else:
                for aloop in adict.block["loops"]:
                    self.AddCifItem((aloop.keys(),aloop.values()))

    def GetCifItem(self,itemname):
        # assume case is correct first
        try:
            return self.block[itemname]
        except KeyError:
            for loop in self.block["loops"]:
                try:
                    return loop[itemname]
                except KeyError:
                    pass
        if itemname.lower() not in self.lower_keys:
            raise KeyError, 'Item %s not in Cif block' % itemname
        # if we are still here, need to check case before raising
        # an error...
        real_keys = self.block.keys()
        lower_keys = map(lambda a:a.lower(),self.block.keys()) 
        try:
            k_index = lower_keys.index(itemname.lower())
        except ValueError:
            pass
        else:             #no exception, can return key
            return self.block[real_keys[k_index]]
        for aloop in self.block["loops"]:
            real_keys = aloop.keys()
            lower_keys = map(lambda a:a.lower(),real_keys)
            try:
                k_index = lower_keys.index(itemname.lower())
            except ValueError:
                pass
            else:             #no exception, have to delete key
                return aloop[real_keys[k_index]]
        raise KeyError, 'Item %s not in Cif block' % itemname

    def RemoveCifItem(self,itemname):
        if itemname.lower() not in self.lower_keys:
            raise KeyError                 # forget it 
        real_keys = self.block.keys()
        lower_keys = map(lambda a:a.lower(),real_keys)
        try:
            k_index = lower_keys.index(itemname.lower())
        except ValueError:
            pass
        else:             #no exception, have to delete key
            del self.block[real_keys[k_index]]
            self.lower_keys.remove(itemname.lower())
            return        #no duplicates, no more checking needed
        for aloop in self.block["loops"]:
            real_keys = aloop.keys()
            lower_keys = map(lambda a:a.lower(),real_keys)
            try:
                k_index = lower_keys.index(itemname.lower())
            except ValueError:
                pass
            else:             #no exception, have to delete key
                del aloop[real_keys[k_index]]
                self.lower_keys.remove(itemname.lower())
                self.block["loops"] = filter(None, self.block["loops"])

    def AddCifItem(self,data):
        # we accept only tuples, strings and lists!!
        if not (isinstance(data[0],StringType) or isinstance(data[0],(TupleType,ListType))):
                  raise TypeError, 'Cif datanames are either a string, tuple or list'
        # now put into the dictionary properly...
        # if we have the case of a single looped item, we allow isolated data names
        # by now making the data name into a list  
        reg_dname = data[0]
        reg_data  = data[1]
        if isinstance(data[1],(ListType,TupleType)) and isinstance(data[0],StringType):# looped values
            reg_dname = [reg_dname]            # process as loop
            reg_data = [reg_data]
        if isinstance(reg_dname,StringType):   # a single name
            self.check_data_name(reg_dname)    # make sure no nasty characters   

            # now make sure the data is OK
            regval = self.regularise_data(data[1])
            self.check_item_value(regval)
            try:
                self.RemoveCifItem(reg_dname)     # may be different case, so have to do this
            except KeyError:
                pass
            self.block.update({reg_dname:regval})  # trust the data is OK
            self.lower_keys.append(reg_dname.lower())
        else:                                # we loop
           if len(reg_dname)!=len(reg_data):
               raise TypeError, 'Length mismatch between itemnames and values'
           dellist = []
           map (self.check_data_name,reg_dname)
           for itemname in reg_dname:
                try:
                    self.RemoveCifItem(itemname)     # may be different case, so have to do this
                except KeyError:
                    pass
           newdict = {}
           proper_vals = map(self.regularise_data,reg_data)
           map(self.check_item_value,proper_vals)
           map(lambda a,b,c=newdict:c.update({a:b}),reg_dname,proper_vals)
           self.block["loops"].append(newdict)
           self.lower_keys.extend(map(lambda a:a.lower(),reg_dname))
        return

    def checklengths(self):
        toolong = filter(lambda a:len(a)>75, self.keys())
        outstring = ""
        for it in toolong: outstring += "\n" + it
        if toolong:
           raise CifError, 'Following data names too long:' + outstring

    def check_data_name(self,dataname): 
        if len(dataname) > 75:
            raise CifError, 'Dataname ' + dataname + ' too long.'
        if dataname[0]!='_':
            raise CifError, 'Dataname ' + dataname + ' does not begin with _'
        if len (filter (lambda a: ord(a) < 33 or ord(a) > 126, dataname)) > 0:
            raise CifError, 'Dataname ' + dataname + ' contains forbidden characters'
     
    def check_item_value(self,item):
        test_item = item
        if type(item) != TupleType and type(item) != ListType:
           test_item = [item]         #single item list
        def check_one (it):
            if type(it) == StringType:
                if len (filter (lambda a:ord(a) != 9 and ord(a) != 10 and ord(a) != 13
                        and (ord(a) < 32 or ord(a) > 126), it)) > 0:
                    raise CifError, 'Data item ' + it + '... contains forbidden characters'
        map(check_one,test_item)

    def regularise_data(self,dataitem):
        alrighttypes = [IntType, LongType, 
                        FloatType, StringType]
        okmappingtypes = [TupleType, ListType]
        thistype = type(dataitem)
        if thistype in alrighttypes or thistype in okmappingtypes:
            return dataitem
        # so try to make into a list
        try:
            regval = list(dataitem)
        except TypeError, value:
            raise CifError, str(dataitem) + ' is wrong type for data value\n' 
        return regval
        
    def GetLoop(self,keyname):
        for aloop in self.block["loops"]:
            lower_keys = map(lambda a:a.lower(),aloop.keys())
            if keyname.lower() in lower_keys:
                return aloop.items()
        # not a looped item
        if self.has_key(itemname):
            raise TypeError, 'Non-looped item'
        raise KeyError, 'Item does not exist'

    def AddToLoop(self,dataname,loopdata):
        found = 0
        for aloop in self.block["loops"]:
            loop_keys = map(lambda a:a.lower(),aloop.keys())
            if dataname.lower() in loop_keys:
                found = 1
                for itemname,itemvalue in loopdata.items():
                    if not isinstance(itemvalue,(ListType,TupleType)):
                        raise CifError, 'AddToLoop given non-list data'
                    if len(itemvalue)!= len(aloop[dataname]):
                        raise CifError, 'Datalength mismatch adding to loop: %s and %s' % (itemname, dataname)
                    aloop.update({itemname:itemvalue})
                    self.lower_keys.append(itemname.lower())
        if not found:
            raise KeyError, 'No such looped item name: %s' % dataname

    def loops(self):
        return map(lambda a:a.keys(),self.block["loops"])

    def merge(self,new_block,mode="strict",match_att="",nosaves=False):
        # deal with save frames
        if not nosaves:
            self["saves"].merge(new_block["saves"],mode,match_att=match_att)
        if mode == 'strict':
           for key in new_block.keys(): 
               if self.has_key(key) and key != match_att:
                  raise CifError, "Identical keys %s in strict merge mode" % key
               elif key != match_att:           #no change otherwise
                  self[key] = new_block[key] 
        if mode == 'replace':
           newkeys = new_block.keys()
           try:
               newkeys.remove(match_att)        #don't touch the special one
           except ValueError:
               pass
           for key in newkeys: self[key] = new_block[key]
        if mode == 'overlay': 
           for attribute in new_block.keys():
               if attribute == match_att: continue      #ignore this one
               new_value = new_block[attribute]
               #non-looped items
               if isinstance(new_value,StringType):
                  self[attribute] = new_value 
           for newloop in new_block.loops(): 
               these_atts = self.keys()
               overlaps = filter(lambda a: a in these_atts,newloop)
               if len(overlaps)< len(newloop):#completely new loop
                  self.AddCifItem((newloop,map(lambda a:new_block[a],newloop)))
               elif len(overlaps)==len(newloop):
                  # appending 
                  overlap_data = map(lambda a:listify(self[a]),overlaps)
                  new_data = map(lambda a:new_block[a],overlaps)
                  packet_data = transpose(overlap_data)
                  new_p_data = transpose(new_data)
                  # wipe out the old data and enter the new stuff
                  self.AddCifItem((newloop,new_data))
                  for pd in packet_data:
                     if pd not in new_p_data:
                        for i in range(len(overlaps)):
                            #don't do this at home; we are appending
                            #to something in place
                            self[overlaps[i]].append(pd[i]) 
                              
    def printsection(self,order=[]):
        import cStringIO
        import string
        # first make an ordering
        if not order:
            order = self.keys()
            order.sort()
        # now prune that ordering...
        order = filter(lambda a,b=self.block:b.has_key(a),order)
        # now do it...
        outstring = cStringIO.StringIO()       # the returned string
        # print any save blocks
        if len(self.block["saves"])>0:
            for savename in self.block["saves"].keys():
               outstring.write("\nsave_%s \n\n" % savename)
               outstring.write(str(self.block["saves"][savename]))
               outstring.write("\n\nsave_\n\n")
        for itemname in order:
            itemvalue = self.block[itemname]
            if isinstance(itemvalue,StringType):
                  thisstring = self._formatstring(itemvalue)
                  if len(thisstring) + len(itemname) < (self.wraplength-2):
                          outstring.write('%s %s\n' % (itemname,thisstring))
                  else:
                          outstring.write('%s\n %s\n' % (itemname, thisstring))
            else: 
                      if len(str(itemvalue)) + len(itemname) < (self.wraplength-2):
                          outstring.write('%s %s\n' % (itemname, itemvalue))
                      else:
                          outstring.write('%s\n %s\n' % (itemname, itemvalue))
            continue
        #do the loops
        for aloop in self.block["loops"]:
               outstring.write('\n loop_\n')
               loopnames = aloop.keys()
               loopnames.sort()
               numdata = len(aloop[loopnames[0]])
               for name in loopnames: 
                   outstring.write('   %-75s\n' % name)
                   if len(aloop[name]) != numdata:
                       raise CifError,'Loop data mismatch for ' + name + \
                       ':output aborted\n'+ '%d , expected %d:' % \
                       (len(aloop[name]),numdata) + `aloop[loopnames[0]]`+`aloop[name]` + outstring.getvalue()
               curstring = ''      
               # when adding to outstring, make sure to add spaces
               for position in range(numdata):
                   for name in loopnames:
                       # at each point, get the next data value
                       datapoint = aloop[name][position]
                       if isinstance(datapoint,StringType):
                           thisstring = '%s' % (self._formatstring(datapoint)) #no spaces yet
                           if '\n' in thisstring:
                               # we try to wrap if the first <eol> is bigger than our wrap length
                               if len(curstring) + string.find(thisstring,'\n') > (self.wraplength):
                                   outstring.write(' ' + curstring + '\n' + thisstring)
                               else:
                                   outstring.write(' ' + curstring + ' ' + thisstring) #a space
                               curstring = ''
                               continue
                       else: 
                           thisstring = ' %s ' % datapoint
                       if len(curstring) + len(thisstring)> self.wraplength-2: #past end of line with space
                           outstring.write(' ' + curstring+'\n') #add the space
                           curstring = ''
                       curstring = curstring + ' ' + thisstring
                   outstring.write(' ' + curstring + '\n')    #last time through
                   curstring = ''
        returnstring = outstring.getvalue()
        outstring.close()
        return returnstring

    def _formatstring(self,instring):
        import string
        if len(instring)< (self.maxoutlength-2) and '\n' not in instring and not ('"' in instring and '\'' in instring):
            if not ' ' in instring and not '\t' in instring and not '\v' \
              in instring and not '_' in instring:                  # no blanks
                return ' %s ' % (instring)
            if not "'" in instring:                                       #use apostrophes
                return "'%s'" % (instring)
            elif not "\"" in instring:
                return '"%s"' % (instring)
        # is a long one or one that needs semicolons due to carriage returns
        outstring = "\n;\n"
        # if there are returns in the string, try to work with them
        while 1:
            retin = string.find(instring,'\n')+1
            if retin < self.maxoutlength and retin > 0:      # honour this break
                outstring = outstring + instring[:retin]
                instring = instring[retin:]
            elif len(instring)<self.maxoutlength:            # finished
                outstring = outstring + instring + '\n;\n'
                break
            else:                             # find a space
                for letter in range(self.maxoutlength-1,40,-1): 
                    if instring[letter] in ' \t\f': break
                outstring = outstring + instring[:letter+1]
                outstring = outstring + '\n'
                instring = instring[letter+1:]            
        return outstring


class CifError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        print '\nCif Format error: '+ self.value 

class ValidCifError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        print '\nCif Validity error: ' + self.value

class CifDic(BlockCollection):
    def __init__(self,dic):
        self.dic_as_cif = dic
        if isinstance(dic,StringType):
            self.dic_as_cif = CifFile(dic)
        (self.dicname,self.diclang,self.defdata) = self.dic_determine(self.dic_as_cif)
        BlockCollection.__init__(self,datasource=self.defdata) 
        # rename and expand out definitions using "_name" in DDL dictionaries
        if self.diclang == "DDL1":
            self.DDL1_normalise()   #this removes any non-definition entries
            self.ddl1_cat_load()
        else:
            self.DDL2_normalise()   #iron out some DDL2 tricky bits
        # initialise type information
        self.typedic={}
        self.primdic = {}   #typecode<->primitive type translation
        self.add_type_info()
        self.add_category_info()
        self.item_validation_funs = [
            self.validate_item_type,
            self.validate_item_esd,
            self.validate_item_enum,   # functions which check conformance
            self.validate_enum_range,
            self.validate_looping]
        self.loop_validation_funs = [
            self.validate_loop_membership,
            self.validate_loop_key,
            self.validate_loop_references]    # functions checking loop values
        self.global_validation_funs = [
            self.validate_exclusion,
            self.validate_parent,
            self.validate_child,
            self.validate_dependents,
            self.validate_uniqueness] # where we need to look at other values
        self.block_validation_funs = [  # where only a full block will do
            self.validate_mandatory_category]
        self.global_remove_validation_funs = [
            self.validate_remove_parent_child] # removal is quicker with special checks
        self.optimize = False        # default value
        self.done_parents = []
        self.done_children = []
        self.done_keys = []
        # debug
        # j = open("dic_debug","w")
        # j.write(self.__str__())
        # j.close()

    def dic_determine(self,cifdic):
        if cifdic.has_key("on_this_dictionary"): 
            self.master_key = "on_this_dictionary"
            self.type_spec = "_type"
            self.enum_spec = "_enumeration"
            self.cat_spec = "_category"
            self.esd_spec = "_type_conditions"
            self.must_loop_spec = "_list"
            self.must_exist_spec = "_list_mandatory"
            self.list_ref_spec = "_list_reference"
            self.unique_spec = "_list_uniqueness"
            self.child_spec = "_list_link_child"
            self.parent_spec = "_list_link_parent"
            self.related_func = "_related_function"
            self.related_item = "_related_item"
            self.primitive_type = "_type"
            self.dep_spec = "xxx"
            self.cat_list = []   #to save searching all the time
            name = cifdic["on_this_dictionary"]["_dictionary_name"]
            version = cifdic["on_this_dictionary"]["_dictionary_version"]
            return (name+version,"DDL1",cifdic)
        elif len(cifdic.keys()) == 1:              # DDL2
            self.master_key = cifdic.keys()[0]      
            name = cifdic[self.master_key]["_dictionary.title"]
            version = cifdic[self.master_key]["_dictionary.version"]
            if name != self.master_key:
                print "Warning: DDL2 blockname %s not equal to dictionary name %s" % (self.master_key,name)
            self.type_spec = "_item_type.code" 
            self.enum_spec = "_item_enumeration.value"
            self.esd_spec = "_item_type_conditions.code"
            self.cat_spec = "_item.category_id" 
            self.loop_spec = "there_is_no_loop_spec!"
            self.must_loop_spec = "xxx"
            self.must_exist_spec = "_item.mandatory_code"
            self.child_spec = "_item_linked.child_name"
            self.parent_spec = "_item_linked.parent_name"
            self.related_func = "_item_related.function_code"
            self.related_item = "_item_related.related_name"
            self.unique_spec = "_category_key.name"
            self.list_ref_spec = "xxx"
            self.primitive_type = "_type"
            self.dep_spec = "_item_dependent.dependent_name"
            return (name+version,"DDL2",cifdic[name]["saves"])
        else:
            raise CifError, "Unable to determine dictionary DDL version"
        
    def DDL1_normalise(self):
        # add default type information in DDL2 style
        # initial types and constructs
        base_types = ["char","numb","null"]
        prim_types = base_types[:] 
        base_constructs = [".*",
            '(-?(([0-9]*[.][0-9]+)|([0-9]+)[.]?)([(][0-9]+[)])?([eEdD][+-]?[0-9]+)?)|\?|\.',
            "\"\" "]
        for key,value in self.dictionary.items():
           if value.has_key("_name"):
               real_name = value["_name"]
               if type(real_name) is ListType:        #looped values
                   for looped_name in real_name:
                       new_value = value.copy()
                       new_value["_name"] = looped_name  #only looped name
                       self.dictionary[looped_name] = new_value
               else: self.dictionary[real_name] = value
           # delete the old one
           del self.dictionary[key]
        # loop again to normalise the contents of each definition
        for key,value in self.dictionary.items():
           # deal with a missing _list, _type_conditions
           if not value.has_key("_list"): value["_list"] = 'no'
           if not value.has_key("_type_conditions"): value["_type_conditions"] = 'none'
           # deal with enumeration ranges
           if value.has_key("_enumeration_range"):
               max,min = self.getmaxmin(value["_enumeration_range"])
               if min == ".":
                   self.dictionary[key].AddCifItem((("_item_range.maximum","_item_range.minimum"),((max,max),(max,min))))
               elif max == ".":
                   self.dictionary[key].AddCifItem((("_item_range.maximum","_item_range.minimum"),((max,min),(min,min))))
               else:
                   self.dictionary[key].AddCifItem((("_item_range.maximum","_item_range.minimum"),((max,max,min),(max,min,min))))
           #add any type construct information
           if value.has_key("_type_construct"):
               base_types.append(value["_name"]+"_type")   #ie dataname_type
               base_constructs.append(value["_type_construct"]+"$")
               prim_types.append(value["_type"])     #keep a record
               value["_type"] = base_types[-1]   #the new type name
               
        
        #make categories conform with ddl2
        #note that we must remove everything from the last underscore
           if value["_category"] == "category_overview":
                last_under = value["_name"].rindex("_")
                catid = value["_name"][1:last_under]
                value["_category.id"] = catid  #remove square bracks
                if catid not in self.cat_list: self.cat_list.append(catid) 
        # we now add any missing categories before filling in the rest of the
        # information
        for key,value in self.dictionary.items():
            if self[key].has_key("_category"):
                if self[key]["_category"] not in self.cat_list:
                    # rogue category, add it in
                    newcat = self[key]["_category"]
                    fake_name = "_" + newcat + "_[]" 
                    newcatdata = CifBlock()
                    newcatdata["_category"] = "category_overview"
                    newcatdata["_category.id"] = newcat
                    newcatdata["_type"] = "null"
                    self[fake_name] = newcatdata
                    self.cat_list.append(newcat)
        # write out the type information in DDL2 style
        self.dic_as_cif[self.master_key].AddCifItem((
            ("_item_type_list.code","_item_type_list.construct",
              "_item_type_list.primitive_code"),
            (base_types,base_constructs,prim_types)
            ))
     
    def DDL2_normalise(self):
       dodgy_defs = filter(lambda a:isinstance(self[a].get('_item.name'),ListType),self.keys()) 
       # now filter out all the single element lists!
       dodgy_defs = filter(lambda a:len(self[a]['_item.name']) > 1, dodgy_defs)
       for item_def in dodgy_defs:
          # print "DDL2 norm: processing %s" % item_def
          thisdef = self[item_def]
          packet_no = thisdef['_item.name'].index(item_def)
          realcat = thisdef['_item.category_id'][packet_no] 
          realmand = thisdef['_item.mandatory_code'][packet_no]
          # first add in all the missing categories
          # we don't replace the entry in the list corresponding to the
          # current item, as that would wipe out the information we want
          for child_no in range(len(thisdef['_item.name'])):
              if child_no == packet_no: continue
              child_name = thisdef['_item.name'][child_no]
              child_cat = thisdef['_item.category_id'][child_no]
              child_mand = thisdef['_item.mandatory_code'][child_no]
              if not self.has_key(child_name):
                  self[child_name] = CifBlock()
                  self[child_name]['_item.name'] = child_name
              self[child_name]['_item.category_id'] = child_cat
              self[child_name]['_item.mandatory_code'] = child_mand
          self[item_def]['_item.name'] = item_def
          self[item_def]['_item.category_id'] = realcat
          self[item_def]['_item.mandatory_code'] = realmand
       # go through any _item_linked tables
       dodgy_defs = filter(lambda a:isinstance(self[a].get('_item_linked.child_name'),ListType),self.keys()) 
       dodgy_defs = filter(lambda a:len(self[a]['_item_linked.child_name']) > 1, dodgy_defs)
       for item_def in dodgy_defs:
          thisdef = self[item_def]
          child_list = thisdef.get('_item_linked.child_name',[])
          parents = thisdef.get('_item_linked.parent_name',[])
          # zap the parents, they will confuse us!!
          del thisdef['_item_linked.parent_name']
          if isinstance(child_list,StringType):
              self[child_list]['_item_linked.parent_name'] = parents
              self[parents]['_item_linked.child_name'] = child_list 
          else:
              # for each parent, find the list of children.
              family = map(None,parents,child_list)
              notmychildren = family
              while len(notmychildren):
                  # get all children of first entry
                  mychildren = filter(lambda a:a[0]==notmychildren[0][0],family)
                  # print "Parent %s: %d children" % (notmychildren[0][0],len(mychildren))
                  for parent,child in mychildren:   #parent is the same for all
                      self[child]['_item_linked.parent_name'] = parent
                  # put all the children into the parent
                  self[mychildren[0][0]]['_item_linked.child_name'] = map(lambda a:a[1],mychildren)
                  # now make a new,smaller list
                  notmychildren = filter(lambda a:a[0]!=mychildren[0][0],notmychildren)
       # next we do aliases
       all_aliases = filter(lambda a:self[a].has_key('_item_aliases.alias_name'),self.keys()) 
       for aliased in all_aliases:
          my_aliases = listify(self[aliased]['_item_aliases.alias_name'])
          for alias in my_aliases:
              self[alias] = self[aliased].copy()   #we are going to delete stuff...
              del self[alias]["_item_aliases.alias_name"]
 
    def ddl1_cat_load(self):
        deflist = self.keys()       #slight optimization
        cat_mand_dic = {}
        cat_unique_dic = {}
        # a function to extract any necessary information from each definition
        def get_cat_info(single_def):
            if self[single_def].get(self.must_exist_spec)=='yes':
                thiscat = self[single_def]["_category"]
                curval = cat_mand_dic.get(thiscat,[])
                curval.append(single_def)
                cat_mand_dic[thiscat] = curval
            # now the unique items...
            # cif_core.dic throws us a curly one: the value of list_uniqueness is
            # not the same as the defined item for publ_body_label, so we have
            # to collect both together.  We assume a non-listed entry, which
            # is true for all current (May 2005) ddl1 dictionaries.
            if self[single_def].get(self.unique_spec,None)!=None:
                thiscat = self[single_def]["_category"]
                new_unique = self[single_def][self.unique_spec]
                uis = cat_unique_dic.get(thiscat,[])
                if single_def not in uis: uis.append(single_def)
                if new_unique not in uis: uis.append(new_unique)
                cat_unique_dic[thiscat] = uis
            
        map(get_cat_info,deflist)       # apply the above function
        for cat in cat_mand_dic.keys():
            self["_" + cat+"_[]"]["_category_mandatory.name"] = cat_mand_dic[cat]
        for cat in cat_unique_dic.keys():
            self["_" + cat+"_[]"]["_category_key.name"] = cat_unique_dic[cat]


    def add_type_info(self):
        if self.dic_as_cif[self.master_key].has_key("_item_type_list.construct"): 
            types = self.dic_as_cif[self.master_key]["_item_type_list.code"]
            prim_types = self.dic_as_cif[self.master_key]["_item_type_list.primitive_code"]
            constructs = map(lambda a: a + "$", self.dic_as_cif[self.master_key]["_item_type_list.construct"])
            # add in \r wherever we see \n, and change \{ to \\{
            def regex_fiddle(mm_regex):
                brack_match = r"((.*\[.+)(\\{)(.*\].*))" 
                ret_match = r"((.*\[.+)(\\n)(.*\].*))" 
                fixed_regexp = mm_regex[:]  #copy
                # fix the brackets
                bm = re.match(brack_match,mm_regex)
                if bm != None: 
                    fixed_regexp = bm.expand(r"\2\\\\{\4")
                # fix missing \r
                rm = re.match(ret_match,fixed_regexp)
                if rm != None:
                    fixed_regexp = rm.expand(r"\2\3\\r\4")    
                #print "Regexp %s becomes %s" % (mm_regex,fixed_regexp)
                return fixed_regexp
            constructs = map(regex_fiddle,constructs)
            packed_up = map(None,types,constructs)
            for typecode,construct in packed_up:
                self.typedic[typecode] = re.compile(construct,re.MULTILINE|re.DOTALL)
            # now make a primitive <-> type construct mapping
            packed_up = map(None,types,prim_types)
            for typecode,primtype in packed_up:
                self.primdic[typecode] = primtype

    def add_category_info(self):
        categories = filter(lambda a:self[a].has_key("_category.id"),self.keys())
        # get the category id
        category_ids = map(lambda a:self[a]["_category.id"],categories)
        # match ids and entries in the dictionary
        catpairs = map(None,category_ids,categories)
        self.cat_map = {}
        for catid,cat in catpairs:self.cat_map[catid] = cat

    def get_number_with_esd(numstring):
        import string
        numb_re = '((-?(([0-9]*[.]([0-9]+))|([0-9]+)[.]?))([(][0-9]+[)])?([eEdD][+-]?[0-9]+)?)|(\?)|(\.)' 
        our_match = re.match(numb_re,numstring)
        if our_match:
            a,base_num,b,c,dad,dbd,esd,exp,q,dot = our_match.groups()
        #    print "Debug: %s -> %s" % (numstring, `our_match.groups()`)
        else:
            return None,None
        if dot or q: return None,None     #a dot or question mark
        if exp:          #has exponent 
           exp = string.replace(exp,"d","e")     # mop up old fashioned numbers
           exp = string.replace(exp,"D","e")
           base_num = base_num + exp
        #print "Debug: have %s for base_num from %s" % (base_num,numstring)
        base_num = float(base_num)
        # work out esd, if present.
        if esd:
            esd = float(esd[1:-1])    # no brackets
            if dad:                   # decimal point + digits
                esd = esd * (10 ** (-1* len(dad)))
            if exp:
                esd = esd * (10 ** (float(exp[1:])))
        return base_num,esd

    def getmaxmin(self,rangeexp):
        regexp = '(-?(([0-9]*[.]([0-9]+))|([0-9]+)[.]?)([eEdD][+-]?[0-9]+)?)*' 
        regexp = regexp + ":" + regexp
        regexp = re.match(regexp,rangeexp)
        try:
            minimum = regexp.group(1)
            maximum = regexp.group(7)
        except AttributeError:
            print "Can't match %s" % rangeexp
        if minimum == None: minimum = "." 
        else: minimum = float(minimum)
        if maximum == None: maximum = "." 
        else: maximum = float(maximum)
        return maximum,minimum

    def validate_item_type(self,item_name,item_value):
        def mymatch(m,a):  
            res = m.match(a)
            if res != None: return res.group() 
            else: return ""
        target_type = self[item_name].get(self.type_spec) 
        if target_type == None:          # e.g. a category definition
            return {"result":True}                  # not restricted in any way
        matchexpr = self.typedic[target_type]
        item_values = listify(item_value)
        #for item in item_values:
            #print "Type match " + item_name + " " + item + ":",
        #skip dots and question marks
        check_all = filter(lambda a: a !="." and a != "?",item_values)
        check_all = filter(lambda a: mymatch(matchexpr,a) != a, check_all)
        if len(check_all)>0: return {"result":False,"bad_values":check_all}
        else: return {"result":True}

    def validate_item_esd(self,item_name,item_value):
        if self[item_name].get(self.primitive_type) != 'numb':
            return {"result":None}
        can_esd = self[item_name].get(self.esd_spec,"none") == "esd" 
        if can_esd: return {"result":True}         #must be OK!
        item_values = listify(item_value)
        check_all = filter(lambda a: get_number_with_esd(a)[1] != None, item_values)
        if len(check_all)>0: return {"result":False,"bad_values":check_all}
        return {"result":True}

    def validate_enum_range(self,item_name,item_value):
        if not self[item_name].has_key("_item_range.minimum") and \
           not self[item_name].has_key("_item_range.maximum"):
            return {"result":None}
        minvals = self[item_name].get("_item_range.minimum",default = ["."])
        maxvals = self[item_name].get("_item_range.maximum",default = ["."])
        def makefloat(a):
            if a == ".": return a
            else: return float(a)
        maxvals = map(makefloat, maxvals)
        minvals = map(makefloat, minvals)
        rangelist = map(None,minvals,maxvals)
        item_values = listify(item_value)
        def map_check(rangelist,item_value):
            if item_value == "?" or item_value == ".": return True
            iv,esd = get_number_with_esd(item_value)
            if iv==None: return None  #shouldn't happen as is numb type
            for lower,upper in rangelist:
                #check the minima
                if lower == ".": lower = iv - 1
                if upper == ".": upper = iv + 1
                if iv > lower and iv < upper: return True
                if upper == lower and iv == upper: return True
            # debug
            # print "Value %s fails range check %d < x < %d" % (item_value,lower,upper)
            return False
        check_all = filter(lambda a,b=rangelist: map_check(b,a) != True, item_values)
        if len(check_all)>0: return {"result":False,"bad_values":check_all}
        else: return {"result":True}
                
    def validate_item_enum(self,item_name,item_value):
        try: 
            enum_list = self[item_name][self.enum_spec][:]
        except KeyError:
            return {"result":None}
        enum_list.append(".")   #default value
        enum_list.append("?")   #unknown
        item_values = listify(item_value)
        #print "Enum check: %s in %s" % (`item_values`,`enum_list`)
        check_all = filter(lambda a: a not in enum_list,item_values)
        if len(check_all)>0: return {"result":False,"bad_values":check_all}
        else: return {"result":True}

    def validate_looping(self,item_name,item_value):
        try:
            must_loop = self[item_name][self.must_loop_spec]
        except KeyError:
            return {"result":None}
        if must_loop == 'yes' and isinstance(item_value,StringType): # not looped
            return {"result":False}      #this could be triggered
        if must_loop == 'no' and not isinstance(item_value,StringType): 
            return {"result":False}
        return {"result":True}


    def validate_loop_membership(self,loop_names):
        try:
            categories = map(lambda a:self[a][self.cat_spec],loop_names)
        except KeyError:       #category is mandatory
            raise ValidCifError, "%s missing from dictionary %s for item in loop containing %s" % (self.cat_spec,self.dicname,loop_names[0])
        bad_items =  filter(lambda a:a != categories[0],categories)
        if len(bad_items)>0:
            return {"result":False,"bad_items":bad_items}
        else: return {"result":True}

    def validate_loop_key(self,loop_names):
        category = self[loop_names[0]][self.cat_spec]
        # find any unique values which must be present 
        entry_name = self.cat_map[category]
        key_spec = self[entry_name].get("_category_mandatory.name",[])
        for names_to_check in key_spec:
            if isinstance(names_to_check,StringType):   #only one
                names_to_check = [names_to_check]
            for loop_key in names_to_check:
                if loop_key not in loop_names: 
                    #is this one of those dang implicit items?
                    if self[loop_key].get(self.must_exist_spec,None) == "implicit":
                        continue          #it is virtually there...
                    alternates = self.get_alternates(loop_key)
                    if alternates == []: 
                        return {"result":False,"bad_items":loop_key}
                    for alt_names in alternates:
                        alt = filter(lambda a:a in loop_names,alt_names)
                        if len(alt) == 0: 
                            return {"result":False,"bad_items":loop_key}  # no alternates   
        return {"result":True}
        
    def validate_loop_references(self,loop_names):
        must_haves = map(lambda a:self[a].get(self.list_ref_spec,None),loop_names)
        must_haves = filter(lambda a:a != None,must_haves)
        # build a flat list.  For efficiency we don't remove duplicates,as
        # we expect no more than the order of 10 or 20 looped names.
        def flat_func(a,b): 
            if isinstance(b,StringType): 
               a.append(b)       #single name
            else:
               a.extend(b)       #list of names
            return a
        flat_mh = reduce(flat_func,must_haves,[])
        group_mh = filter(lambda a:a[-1]=="_",flat_mh)
        single_mh = filter(lambda a:a[-1]!="_",flat_mh)
        res = filter(lambda a: a not in loop_names,single_mh)
        def check_gr(s_item, name_list):
            nl = map(lambda a:a[:len(s_item)],name_list)
            if s_item in nl: return True
            return False
        res_g = filter(lambda a:check_gr(a,loop_names),group_mh)
        if len(res) == 0 and len(res_g) == 0: return {"result":True}
        # construct alternate list
        alternates = map(lambda a: (a,self.get_alternates(a)),res)
        alternates = filter(lambda a:a[1] != [], alternates)
        # next two lines purely for error reporting
        missing_alts = filter(lambda a: a[1] == [], alternates)
        missing_alts = map(lambda a:a[0],missing_alts)
        if len(alternates) != len(res): 
           return {"result":False,"bad_items":missing_alts}   #short cut; at least one
                                                       #doesn't have an altern
        #loop over alternates
        for orig_name,alt_names in alternates:
             alt = filter(lambda a:a in loop_names,alt_names)
             if len(alt) == 0: return {"result":False,"bad_items":orig_name}# no alternates   
        return {"result":True}        #found alternates
             
    def get_alternates(self,main_name,exclusive_only=False):
        alternates = self[main_name].get(self.related_func,None)
        alt_names = []
        if alternates != None: 
            alt_names =  self[main_name].get(self.related_item,None)
            if isinstance(alt_names,StringType): 
                alt_names = [alt_names]
                alternates = [alternates]
            together = map(None,alt_names,alternates)
            if exclusive_only:
                alt_names = filter(lambda a:a[1]=="alternate_exclusive" \
                                             or a[1]=="replace", together)
            else:
                alt_names = filter(lambda a:a[1]=="alternate" or a[1]=="replace",together)
            alt_names = map(lambda a:a[0],alt_names)
        # now do the alias thing
        alias_names = listify(self[main_name].get("_item_aliases.alias_name",[]))
        alt_names.extend(alias_names)
        # print "Alternates for %s: %s" % (main_name,`alt_names`)
        return alt_names
        

    def validate_exclusion(self,item_name,item_value,whole_block,provisional_items={},globals={}):
       alternates = map(lambda a:a.lower(),self.get_alternates(item_name,exclusive_only=True))
       item_name_list = map(lambda a:a.lower(),whole_block.keys())
       item_name_list.extend(map(lambda a:a.lower(),provisional_items.keys()))
       item_name_list.extend(map(lambda a:a.lower(),globals.keys()))
       bad = filter(lambda a:a in item_name_list,alternates)
       if len(bad)>0:
           print "Bad: %s, alternates %s" % (`bad`,`alternates`)
           return {"result":False,"bad_items":bad}
       else: return {"result":True}

    # validate that parent exists and contains matching values
    def validate_parent(self,item_name,item_value,whole_block,provisional_items={},globals={}):
        parent_item = self[item_name].get(self.parent_spec)
        if not parent_item: return {"result":None}   #no parent specified
        if isinstance(parent_item,ListType): 
            parent_item = parent_item[0]
        if self.optimize:
            if parent_item in self.done_parents:
                return {"result":None}
            else: 
                self.done_parents.append(parent_item)
                print "Done parents %s" % `self.done_parents`
        # initialise parent/child values
        if isinstance(item_value,StringType):
            child_values = [item_value]
        else: child_values = item_value[:]    #copy for safety
        # track down the parent
        # print "Looking for %s parent item %s in %s" % (item_name,parent_item,`whole_block`)
        # if globals contains the parent values, we are doing a DDL2 dictionary, and so 
        # we have collected all parent values into the global block - so no need to search
        # for them elsewhere. 
        # print "Looking for %s" % `parent_item`
        parent_values = globals.get(parent_item)
        if not parent_values:
            parent_values = provisional_items.get(parent_item,whole_block.get(parent_item))
        if not parent_values:  
            # go for alternates
            namespace = whole_block.keys()
            namespace.extend(provisional_items.keys())
            namespace.extend(globals.keys())
            alt_names = filter_present(self.get_alternates(parent_item),namespace)
            if len(alt_names) == 0:
                if len(filter(lambda a:a != "." and a != "?",child_values))>0:
                    return {"result":False,"parent":parent_item}#no parent available -> error
                else:
                    return {"result":None}       #maybe True is more appropriate??
            parent_item = alt_names[0]           #should never be more than one?? 
            parent_values = provisional_items.get(parent_item,whole_block.get(parent_item))
            if not parent_values:   # check global block
                parent_values = globals.get(parent_item)
        if isinstance(parent_values,StringType):
            parent_values = [parent_values]   
        #print "Checking parent %s against %s, values %s/%s" % (parent_item,
        #                                          item_name,`parent_values`,`child_values`)
        missing = self.check_parent_child(parent_values,child_values)
        if len(missing) > 0:
            return {"result":False,"bad_values":missing,"parent":parent_item}
        return {"result":True}

    def validate_child(self,item_name,item_value,whole_block,provisional_items={},globals={}):
        try:
            child_items = self[item_name][self.child_spec][:]  #copy
        except KeyError:
            return {"result":None}    #not relevant
        # special case for dictionaries  -> we check parents of children only
        if globals.has_key(item_name):  #dictionary so skip
            return {"result":None}
        if isinstance(child_items,StringType): # only one child
            child_items = [child_items]
        if isinstance(item_value,StringType): # single value
            parent_values = [item_value]
        else: parent_values = item_value[:]
        # expand child list with list of alternates
        for child_item in child_items[:]:
            child_items.extend(self.get_alternates(child_item))
        # now loop over the children
        for child_item in child_items:
            if self.optimize:
                if child_item in self.done_children:
                    return {"result":None}
                else: 
                    self.done_children.append(child_item)
                    print "Done children %s" % `self.done_children`
            if provisional_items.has_key(child_item):
                child_values = provisional_items[child_item][:]
            elif whole_block.has_key(child_item):
                child_values = whole_block[child_item][:]
            else:  continue 
            if isinstance(child_values,StringType):
                child_values = [child_values]
            #    print "Checking child %s against %s, values %s/%s" % (child_item,
            #                                          item_name,`child_values`,`parent_values`)
            missing = self.check_parent_child(parent_values,child_values)
            if len(missing)>0:
                return {"result":False,"bad_values":missing,"child":child_item}
        return {"result":True}       #could mean that no child items present
           
    #a generic checker: all child vals should appear in parent_vals
    def check_parent_child(self,parent_vals,child_vals):
        # shield ourselves from dots and question marks
        pv = parent_vals[:]
        pv.extend([".","?"])
        res =  filter(lambda a:a not in pv,child_vals)
        #print "Missing: %s" % res
        return res

    def validate_remove_parent_child(self,item_name,whole_block):
        try:
            child_items = self[item_name][self.child_spec]
        except KeyError:
            return {"result":None}
        if isinstance(child_items,StringType): # only one child
            child_items = [child_items]
        for child_item in child_items:
            if whole_block.has_key(child_item): 
                return {"result":False,"child":child_item}
        return {"result":True}
         
    def validate_dependents(self,item_name,item_value,whole_block,prov={},globals={}):
        try:
            dep_items = self[item_name][self.dep_spec][:]
        except KeyError:
            return {"result":None}    #not relevant
        if isinstance(dep_items,StringType):
            dep_items = [dep_items]
        actual_names = whole_block.keys()
        actual_names.extend(prov.keys())
        actual_names.extend(globals.keys())
        missing = filter(lambda a:a not in actual_names,dep_items)
        if len(missing) > 0:
            alternates = map(lambda a:[self.get_alternates(a),a],missing)
            # compact way to get a list of alternative items which are 
            # present
            have_check = map(lambda b:[filter_present(b[0],actual_names),
                                       b[1]],alternates) 
            have_check = filter(lambda a:len(a[0])==0,have_check)
            if len(have_check) > 0:
                have_check = map(lambda a:a[1],have_check)
                return {"result":False,"bad_items":have_check}
        return {"result":True}
        
    def validate_uniqueness(self,item_name,item_value,whole_block,provisional_items={},
                                                                  globals={}):
        category = self[item_name].get(self.cat_spec)
        if category == None:
            print "No category found for %s" % item_name
            return {"result":None}
        # print "Category %s for item %s" % (`category`,item_name)
        catentry = self.cat_map[category]
        # we make a copy in the following as we will be removing stuff later!
        unique_i = self[catentry].get("_category_key.name",[])[:]
        if isinstance(unique_i,StringType):
            unique_i = [unique_i]
        if item_name not in unique_i:       #no need to verify
            return {"result":None}
        if isinstance(item_value,StringType):  #not looped
            return {"result":None}
        # print "Checking %s -> %s -> %s ->Unique: " % (item_name,category,catentry) + `unique_i`
        # check that we can't optimize by not doing this check
        if self.optimize:
            if unique_i in self.done_keys:
                return {"result":None}
            else:
                self.done_keys.append(unique_i)
        val_list = []
        # get the matching data from any other data items
        unique_i.remove(item_name)
        other_data = []
        if len(unique_i) > 0:            # i.e. do have others to think about
           for other_name in unique_i:
           # we look for the value first in the provisional dict, then the main block
           # the logic being that anything in the provisional dict overrides the
           # main block
               if provisional_items.has_key(other_name):
                   other_data.append(provisional_items[other_name]) 
               elif whole_block.has_key(other_name):
                   other_data.append(whole_block[other_name])
               elif self[other_name].get(self.must_exist_spec)=="implicit":
                   other_data.append([item_name]*len(item_value))  #placeholder
               else:
                   return {"result":False,"bad_items":other_name}#missing data name
        # ok, so we go through all of our values
        # this works by comparing lists of strings to one other, and
        # so could be fooled if you think that '1.' and '1' are 
        # identical
        for i in range(len(item_value)):
            #print "Value no. %d" % i ,
            this_entry = item_value[i]
            for j in range(len(other_data)):
                this_entry = " ".join([this_entry,other_data[j][i]]) 
            #print "Looking for %s in %s: " % (`this_entry`,`val_list`)
            if this_entry in val_list: 
                return {"result":False,"bad_values":this_entry}
            val_list.append(this_entry)
        return {"result":True}


    def validate_mandatory_category(self,whole_block,globals={}):
        mand_cats = filter(lambda a:self[a].get("_category.mandatory_code","no")=="yes",
                    self.keys())
        # map to actual ids
        catlist = self.cat_map.items()
        # print "Mandatory categories - %s" % `mand_cats`
        for mand_cat in mand_cats:
            cat_id = filter(lambda a:a[1]==mand_cat,catlist)[0][0]
            all_keys = whole_block.keys()
            if globals:         #
                all_keys.extend(globals.keys())
            no_of_items = len(filter(lambda a:self[a].get(self.cat_spec)==cat_id,
                                 all_keys))
            if no_of_items == 0:
                return {"result":False,"bad_items":cat_id}
        return {"result":True}


    def run_item_validation(self,item_name,item_value):
        return {item_name:map(lambda f:(f.__name__,f(item_name,item_value)),self.item_validation_funs)}

    def run_loop_validation(self,loop_names):
        return {loop_names[0]:map(lambda f:(f.__name__,f(loop_names)),self.loop_validation_funs)}

    def run_global_validation(self,item_name,item_value,data_block,provisional_items={},globals={}):
        results = map(lambda f:(f.__name__,f(item_name,item_value,data_block,provisional_items,globals)),self.global_validation_funs)
        return {item_name:results}

    def run_block_validation(self,whole_block,globals={}):
        results = map(lambda f:(f.__name__,f(whole_block,globals)),self.block_validation_funs)
        # fix up the return values
        return {"whole_block":results}

    def optimize_on(self):
        self.optimize = True
        self.done_keys = []
        self.done_children = []
        self.done_parents = []

    def optimize_off(self):
        self.optimize = False
        self.done_keys = []
        self.done_children = []
        self.done_parents = []


class ValidCifBlock(CifBlock):
    def __init__(self,dic = None, diclist=[], mergemode = "replace",*args,**kwords):
        CifBlock.__init__(self,*args,**kwords)    
        if dic and diclist:
            print "Warning: diclist argument ignored when initialising ValidCifBlock"
        if isinstance(dic,CifDic):
            self.fulldic = dic
        else:
            raise TypeError, "ValidCifBlock passed non-CifDic type in dic argument"
        if len(diclist)==0 and not dic:
            raise ValidCifError, "At least one dictionary must be specified"
        if diclist and not dic:
            self.fulldic = merge_dic(diclist,mergemode)
        if not self.run_data_checks()[0]:
            raise ValidCifError, self.report()

    def run_data_checks(self,verbose=False):
        self.v_result = {}
        self.fulldic.optimize_on()
        for dataname in self.keys():
            update_value(self.v_result,self.fulldic.run_item_validation(dataname,self[dataname]))
            update_value(self.v_result,self.fulldic.run_global_validation(dataname,self[dataname],self))
        for loop in self.loops():
            update_value(self.v_result,self.fulldic.run_loop_validation(loop))
        # now run block-level checks
        update_value(self.v_result,self.fulldic.run_block_validation(self))
        # return false and list of baddies if anything didn't match
        self.fulldic.optimize_off()
        for test_key in self.v_result.keys():
            #print "%s: %s" % (test_key,`self.v_result[test_key]`)
            self.v_result[test_key] = filter(lambda a:a[1]["result"]==False,self.v_result[test_key])
            if len(self.v_result[test_key]) == 0: 
                del self.v_result[test_key]
        isvalid = len(self.v_result)==0
        #if not isvalid:
        #    print "Baddies:" + `self.v_result`
        return isvalid,self.v_result

    def single_item_check(self,item_name,item_value):
        #self.match_single_item(item_name)
        if not self.fulldic.has_key(item_name):
            result = {item_name:[]}
        else:
            result = self.fulldic.run_item_validation(item_name,item_value)
        baddies = filter(lambda a:a[1]["result"]==False, result[item_name])
        # if even one false one is found, this should trigger
        isvalid = (len(baddies) == 0)
        # if not isvalid: print "Failures for %s:" % item_name + `baddies`
        return isvalid,baddies

    def loop_item_check(self,loop_names):
        in_dic_names = filter(lambda a:self.fulldic.has_key(a),loop_names)
        if len(in_dic_names)==0:
            result = {loop_names[0]:[]}
        else:
            result = self.fulldic.run_loop_validation(in_dic_names)
        baddies = filter(lambda a:a[1]["result"]==False,result[in_dic_names[0]])
        # if even one false one is found, this should trigger
        isvalid = (len(baddies) == 0)
        # if not isvalid: print "Failures for %s:" % `loop_names` + `baddies`
        return isvalid,baddies

    def global_item_check(self,item_name,item_value,provisional_items={}):
        if not self.fulldic.has_key(item_name):
            result = {item_name:[]}
        else:
            result = self.fulldic.run_global_validation(item_name,
               item_value,self,provisional_items = provisional_items)
        baddies = filter(lambda a:a[1]["result"]==False,result[item_name])
        # if even one false one is found, this should trigger
        isvalid = (len(baddies) == 0)
        # if not isvalid: print "Failures for %s:" % item_name + `baddies`
        return isvalid,baddies

    def remove_global_item_check(self,item_name):
        if not self.fulldic.has_key(item_name):
            result = {item_name:[]}
        else:
            result = self.fulldic.run_remove_global_validation(item_name,self,False)
        baddies = filter(lambda a:a[1]["result"]==False,result[item_name])
        # if even one false one is found, this should trigger
        isvalid = (len(baddies) == 0)
        # if not isvalid: print "Failures for %s:" % item_name + `baddies`
        return isvalid,baddies

    def AddToLoop(self,dataname,loopdata):
        # single item checks
        paired_data = loopdata.items()
        for name,value in paired_data:
            valid,problems = self.single_item_check(name,value) 
            self.report_if_invalid(valid,problems)
        # loop item checks; merge with current loop
        found = 0
        for aloop in self.block["loops"]:
            if aloop.has_key(dataname):
                loopnames = aloop.keys()
                for new_name in loopdata.keys():
                    if new_name not in loopnames: loopnames.append(new_name)
                valid,problems = self.looped_item_check(loopnames)
                self.report_if_invalid(valid,problems)
        prov_dict = loopdata.copy()
        for name,value in paired_data: 
            del prov_dict[name]   # remove temporarily
            valid,problems = self.global_item_check(name,value,prov_dict)
            prov_dict[name] = value  # add back in
            self.report_if_invalid(valid,problems)
        CifBlock.AddToLoop(self,dataname,loopdata)
 
    def AddCifItem(self,data):
        if isinstance(data[0],StringType):   # single item
            valid,problems = self.single_item_check(data[0],data[1])
            self.report_if_invalid(valid,problems,data[0])
            valid,problems = self.global_item_check(data[0],data[1])
            self.report_if_invalid(valid,problems,data[0])
        elif isinstance(data[0],TupleType) or isinstance(data[0],ListType):
            paired_data = map(None,data[0],data[1])
            for name,value in paired_data:
                valid,problems = self.single_item_check(name,value) 
                self.report_if_invalid(valid,problems,name)
            valid,problems = self.loop_item_check(data[0])
            self.report_if_invalid(valid,problems,data[0])
            prov_dict = {}            # for storing temporary items
            for name,value in paired_data: prov_dict[name]=value
            for name,value in paired_data: 
                del prov_dict[name]   # remove temporarily
                valid,problems = self.global_item_check(name,value,prov_dict)
                prov_dict[name] = value  # add back in
                self.report_if_invalid(valid,problems,name)
        CifBlock.AddCifItem(self,data)

    # utility function
    def report_if_invalid(self,valid,bad_list,data_name):
        if not valid:
            error_string = reduce(lambda a,b: a + "," + b[0], bad_list, "") 
            error_string = `data_name` + " fails following validity checks: "  + error_string
            raise ValidCifError, error_string

    def __delitem__(self,key):
        # we don't need to run single item checks; we do need to run loop and
        # global checks.
        if self.has_key(key):
            try: 
                loop_items = self.GetLoop(key)
            except TypeError:
                loop_items = []
            if loop_items:             #need to check loop conformance
                loop_names = map(lambda a:a[0],loop_items)
                loop_names = filter(lambda a:a != key,loop_names)
                valid,problems = self.loop_item_check(loop_names)
                self.report_if_invalid(valid,problems)
            valid,problems = self.remove_global_item_check(key)
            self.report_if_invalid(valid,problems)
        self.RemoveCifItem(key)


    def report(self):
       import cStringIO
       outstr = cStringIO.StringIO()
       outstr.write( "Validation results\n")
       outstr.write( "------------------\n")
       print "%d invalid items found\n" % len(self.v_result)
       for item_name,val_func_list in self.v_result.items():
           outstr.write("%s fails following tests:\n" % item_name)
           for val_func in val_func_list:
               outstr.write("\t%s\n")
       return outstr.getvalue()


class ValidCifFile(CifFile):
    def __init__(self,dic=None,diclist=[],mergemode="replace",*args,**kwargs):
        CifFile.__init__(self,*args,**kwargs)
        if not diclist and not dic:
            raise ValidCifError, "At least one dictionary is required to create a ValidCifFile object"
        if not dic and diclist:     #merge here for speed
            self.bigdic = merge_dic(diclist,mergemode)
        elif dic and not diclist:
            self.bigdic = dic
        for blockname in self.keys():
            self.dictionary[blockname]=ValidCifBlock(data=self.dictionary[blockname],dic=self.bigdic)

    def NewBlock(self,blockname,blockcontents,**kwargs):
        CifFile.NewBlock(self,blockname,blockcontents,**kwargs)
        # dictionary[blockname] is now a CifBlock object.  We
        # turn it into a ValidCifBlock object
        self.dictionary[blockname] = ValidCifBlock(dic=self.bigdic,
                                         data=self.dictionary[blockname])


def validate(ciffile,dic = "", diclist=[],mergemode="replace",isdic=False):
    check_file = CifFile(ciffile)
    if not dic:
        fulldic = merge_dic(diclist,mergemode)
    else:
        fulldic = dic
    no_matches = {}
    valid_result = {}
    if isdic:          #assume one block only
        blockname = check_file.keys()[0]
        check_bc = check_file[blockname]["saves"]
        check_globals = check_file[blockname] 
        # collect a list of parents for speed
        poss_parents = fulldic.get_all("_item_linked.parent_name")
        for parent in poss_parents:
            curr_parent = listify(check_globals.get(parent,[]))
            new_vals = check_bc.get_all(parent)
            new_vals.extend(curr_parent)
            if len(new_vals)>0:
                check_globals[parent] = new_vals
                # print "Added %s (len %d)" % (parent,len(check_globals[parent]))
    else:
        check_bc = check_file
        check_globals = CifBlock()   #empty
    for block in check_bc.keys(): 
        #print "Validating block %s" % block 
        no_matches[block] = filter(lambda a:not fulldic.has_key(a),check_bc[block].keys())
        # remove non-matching items
        # print "Not matched: " + `no_matches[block]`
        for nogood in no_matches[block]:
             del check_bc[block][nogood]
        valid_result[block] = run_data_checks(check_bc[block],fulldic,globals=check_globals)
    return valid_result,no_matches

def validate_report(val_result):
    import cStringIO
    valid_result,no_matches = val_result
    outstr = cStringIO.StringIO()
    outstr.write( "Validation results\n")
    outstr.write( "------------------\n")
    for block in valid_result.keys():
        block_result = valid_result[block]
        if block_result[0]:
            outstr.write( "\n Block %s is VALID\n" % block)
        else: 
            outstr.write( "\n Block %s is INVALID\n" % block)
        if len(no_matches[block])!= 0:
            outstr.write( "\n The following items were not found in the dictionary:\n")
            map(lambda it:outstr.write("%s\n" % it),no_matches[block])
        # now organise our results by type of error, not data item...
        error_type_dic = {}
        for error_item, error_list in block_result[1].items():
            for func_name,bad_result in error_list:
                bad_result.update({"item_name":error_item})
                try:
                    error_type_dic[func_name].append(bad_result)
                except KeyError:
                    error_type_dic[func_name] = [bad_result]
        # make a table of test name, test message
        info_table = {\
        'validate_item_type':\
            "The following data items had badly formed values",
        'validate_item_esd':\
            "The following data items should not have esds appended",
        'validate_enum_range':\
            "The following data items have values outside permitted range",
        'validate_item_enum':\
            "The following data items have values outside permitted set",
        'validate_looping':\
            "The following data items violate looping constraints",
        'validate_loop_membership':\
            "The following looped data names are of different categories to the first looped data name",
        'validate_loop_key':\
            "A required dataname for this category is missing from the loop\n containing the dataname",
        'validate_loop_references':\
            "A dataname required by the item is missing from the loop",
        'validate_parent':\
            "A parent dataname is missing or contains different values",
        'validate_child':\
            "A child dataname contains different values to the parent",
        'validate_uniqueness':\
            "One or more data items do not take unique values",
        'validate_dependents':\
            "A dataname required by the item is missing from the data block",
        'validate_exclusion': \
            "Both dataname and exclusive alternates or aliases are present in data block",
        'validate_mandatory_category':\
            "A required category is missing from this block"}

        for test_name,test_results in error_type_dic.items():
           outstr.write(error_report(test_name,info_table[test_name],test_results)) 
           outstr.write("\n\n")
    return outstr.getvalue()
         
# A function to lay out a single error report.  We are passed
# the name of the error (one of our validation functions), the
# explanation to print out, and a dictionary with the error 
# information

def error_report(error_name,error_explanation,error_dics):
   retstring = "\n\n " + error_explanation + ":\n\n"
   headstring = "%-32s" % "Item name"
   bodystring = ""
   if error_dics[0].has_key("bad_values"):
      headstring += "%-20s" % "Bad value(s)"
   if error_dics[0].has_key("bad_items"):
      headstring += "%-20s" % "Bad dataname(s)"
   if error_dics[0].has_key("child"):
      headstring += "%-20s" % "Child"
   if error_dics[0].has_key("parent"):
      headstring += "%-20s" % "Parent" 
   headstring +="\n"
   for error in error_dics:
      bodystring += "\n%-32s" % error["item_name"]
      if error.has_key("bad_values"):
          bodystring += "%-20s" % error["bad_values"]
      if error.has_key("bad_items"):
          bodystring += "%-20s" % error["bad_items"]
      if error.has_key("child"):
          bodystring += "%-20s" % error["child"]
      if error.has_key("parent"):
          bodystring += "%-20s" % error["parent"]
   return retstring + headstring + bodystring 

def run_data_checks(check_block,fulldic,globals={}):
    v_result = {}
    for key in check_block.keys():
        update_value(v_result, fulldic.run_item_validation(key,check_block[key]))
        update_value(v_result, fulldic.run_global_validation(key,check_block[key],check_block,globals=globals))
    for loop in check_block.loops():
        update_value(v_result, fulldic.run_loop_validation(loop))
    update_value(v_result,fulldic.run_block_validation(check_block,globals=globals))
    # return false and list of baddies if anything didn't match
    for test_key in v_result.keys():
        v_result[test_key] = filter(lambda a:a[1]["result"]==False,v_result[test_key])
        if len(v_result[test_key]) == 0: 
            del v_result[test_key]
    # if even one false one is found, this should trigger
    # print "Baddies:" + `v_result`
    isvalid = len(v_result)==0
    return isvalid,v_result
    

def get_number_with_esd(numstring):
    import string
    numb_re = '((-?(([0-9]*[.]([0-9]+))|([0-9]+)[.]?))([(][0-9]+[)])?([eEdD][+-]?[0-9]+)?)|(\?)|(\.)' 
    our_match = re.match(numb_re,numstring)
    if our_match:
        a,base_num,b,c,dad,dbd,esd,exp,q,dot = our_match.groups()
    #    print "Debug: %s -> %s" % (numstring, `our_match.groups()`)
    else:
        return None,None
    if dot or q: return None,None     #a dot or question mark
    if exp:          #has exponent 
       exp = string.replace(exp,"d","e")     # mop up old fashioned numbers
       exp = string.replace(exp,"D","e")
       base_num = base_num + exp
    #print "Debug: have %s for base_num from %s" % (base_num,numstring)
    base_num = float(base_num)
    # work out esd, if present.
    if esd:
        esd = float(esd[1:-1])    # no brackets
        if dad:                   # decimal point + digits
            esd = esd * (10 ** (-1* len(dad)))
        if exp:
            esd = esd * (10 ** (float(exp[1:])))
    return base_num,esd

# A utility function to append to item values rather than replace them
def update_value(base_dict,new_items):
    for new_key in new_items.keys():
        if base_dict.has_key(new_key):
            base_dict[new_key].extend(new_items[new_key])
        else:
            base_dict[new_key] = new_items[new_key]

#Transpose the list of lists passed to us
def transpose(base_list):
    new_lofl = []
    full_length = len(base_list)
    opt_range = range(full_length)
    for i in range(len(base_list[0])):
       new_packet = [] 
       for j in opt_range:
          new_packet.append(base_list[j][i])
       new_lofl.append(new_packet)
    return new_lofl

# listify strings - used surprisingly often
def listify(item):
    if isinstance(item,StringType): return [item]
    else: return item

# given a list of search items, return a list of items 
# actually contained in the given data block
def filter_present(namelist,datablocknames):
    return filter(lambda a:a in datablocknames,namelist)

# merge ddl dictionaries.  We should be passed filenames or CifFile
# objects
def merge_dic(diclist,mergemode="replace",ddlspec=None):
    dic_as_cif_list = []
    for dic in diclist:
        if not isinstance(dic,CifFile) and \
           not isinstance(dic,StringType):
               raise TypeError, "Require list of CifFile names/objects for dictionary merging"
        if not isinstance(dic,CifFile): dic_as_cif_list.append(CifFile(dic))
        else: dic_as_cif_list.append(dic)
    # we now merge left to right
    basedic = dic_as_cif_list[0]
    if basedic.has_key("on_this_dictionary"):   #DDL1 style only
        for dic in dic_as_cif_list[1:]:
           basedic.merge(dic,mode=mergemode,match_att="_name")
    elif len(basedic.keys()) == 1:                     #One block: DDL2 style
        old_block = basedic[basedic.keys()[0]]
        for dic in dic_as_cif_list[1:]:
           new_block = dic[dic.keys()[0]]
           basedic.merge(dic,mode=mergemode,
                         single_block=[old_block,new_block],
                         match_att="_item.name")
    return CifDic(basedic)


