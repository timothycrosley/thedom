import cPickle as pickle
import gc
import sys
import time

from WebElements import UITemplate
from WebElements.DictUtils import OrderedDict
from WebElements.All import Factory, DOM
from WebElements.Base import WebElement, TemplateElement, TextNode
from WebElements.Layout import Box
from WebElements.Resources import ScriptContainer

results = {'loopedCreate':0.0, 'loopedInit':0.0, 'loopedToHtml':0.0, 'bigTable':0.0, 'bigTableSize':0.0,
           'createAllOnce':0.0, 'longestCreationTime':0.0, 'nestedNodeCreation':0.0,
           'templateInit':0.0, 'templateToHtml':0.0, 'templateToHtmlSize':0.0, 'templateCreate':0.0}

def doneSection():
    sys.stdout.write(".")
    sys.stdout.flush()

def getSingleElementGenerationTimes():
    generationTimes = OrderedDict()
    for product in Factory.products.keys():
        if "." in product:
            continue
        doneSection()
        startTime = time.time()
        scripts = ScriptContainer()
        element = Factory.build(product, 'Test', 'Product')
        element.setScriptContainer(scripts)
        html = element.toHtml()
        html += scripts.toHtml()

        generationTime = time.time() - startTime
        results['createAllOnce'] += generationTime
        generationTimes[generationTime] = (product, len(html))
    results['longestCreationTime'] = generationTimes.orderedKeys[-1]
    return generationTimes

def getGenerationTimeForAllElementsLooped100Times():
    startTime = time.time()
    allProducts = Box('AllProducts')
    scripts = ScriptContainer()
    allProducts.setScriptContainer(scripts)
    for x in xrange(100):
        doneSection()
        results['loopedCreate'] = results['loopedInit'] + results['loopedToHtml']
        for product in Factory.products.keys():
            allProducts.addChildElement(Factory.build(product, 'Test', 'Product'))
    instantiationTime = time.time() - startTime
    results['loopedInit'] = instantiationTime

    startTime = time.time()
    html = allProducts.toHtml()
    html += scripts.toHtml()
    generationTime = (time.time() - startTime)
    results['loopedToHtml'] = generationTime
    results['loopedToHtmlSize'] = len(html)
    results['loopedCreate'] = results['loopedInit'] + results['loopedToHtml']

def getTemplateGenerationTimes():
    template = "div#AllProducts\n"
    templateElements = []
    for product in Factory.products.keys():
        template += "  > %(product)s#test%(product)s\n" % {'product': product}
    template = UITemplate.fromSHPAML(template)

    startTime = time.time()
    for x in xrange(100):
        templateElement = TemplateElement(template=template, factory=Factory)
        templateElement.setScriptContainer(templateElement.addChildElement(ScriptContainer()))
        templateElements.append(templateElement)
        doneSection()
    results['templateInit'] = time.time() - startTime

    html = ""
    startTime = time.time()
    for templateElement in templateElements:
        html += templateElement.toHtml()
        doneSection()

    generationTime = (time.time() - startTime)
    results['templateToHtml'] = generationTime
    results['templateToHtmlSize'] = len(html)
    results['templateCreate'] = results['templateInit'] + results['templateToHtml']

def getBigTableGenerationTime():
    template = UITemplate.fromSHPAML("> dom-table#bigTableTest")
    table = [dict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10) for x in xrange(1000)]

    startTime = time.time()
    templateElement = TemplateElement(template=template, factory=Factory)
    for rowData in table:
        row = templateElement.bigTableTest.addChildElement(DOM.TR())
        for data in rowData.itervalues():
            row.addChildElement(DOM.TD()).addChildElement(TextNode(data))
        doneSection()
    html = templateElement.toHtml()
    results['bigTable'] = time.time() - startTime
    results['bigTableSize'] = len(html)

def getNestedElementTime():
    startTime = time.time()
    rootElement = WebElement('root')
    element = rootElement
    element.tagName = "root"
    html = ""
    for x in xrange(900):
        doneSection()
        element = element.addChildElement(WebElement("element" + str(x)))
        element.tagName = 'tag' + str(x)
        html += element.toHtml()

    results['nestedNodeCreation'] = time.time() - startTime
    results['nestedNodeSize'] = len(html)

if __name__ == "__main__":
    sys.stdout.write("Benchmarking .")
    doneSection()
    getGenerationTimeForAllElementsLooped100Times()
    gc.collect()
    doneSection()
    getTemplateGenerationTimes()
    gc.collect()
    results['generationTimes'] = getSingleElementGenerationTimes()
    gc.collect()
    doneSection()
    getNestedElementTime()
    gc.collect()
    doneSection()
    getBigTableGenerationTime()

    print "."

    print "######## Indvidual element generation times ########"
    results['generationTimes'].orderedKeys.sort()
    for generationTime, info in results['generationTimes'].iteritems():
        print "    Generating html for %s took %s seconds and produced %d len html" % (info[0], generationTime, info[1])
    print "    Total Time: %s" % results['createAllOnce']

    print "######## Looped creation time (%d elements) ########" %  len(Factory.products.keys() * 100)
    print "    Instantiating Elements: " + str(results['loopedInit'])
    print "    Generating Html: " + str(results['loopedToHtml'])
    print "    Html Size: " + str(results['loopedToHtmlSize'] / 1024.0 / 1024.0) + " MB"
    print "    Total Time:" + str(results['loopedCreate'])

    print "######## Template creation time (%d elements) ########" %  len(Factory.products.keys() * 100)
    print "    Instantiating Template: " + str(results['templateInit'])
    print "    Generating Html: " + str(results['templateToHtml'])
    print "    Html Size: " + str(results['templateToHtmlSize'] / 1024.0 / 1024.0) + " MB"
    print "    Total Time:" + str(results['templateCreate'])

    print "######## Nested element generation #########"
    print "    Generating 900 nested elements took: " + str(generationTime)
    print "    Html Size: ", results['nestedNodeSize']

    print "######## Big table generation #########"
    print "    Generating a 10X1000 table took: " + str(results['bigTable'])
    print "    Html Size: ", str(results['bigTableSize'] / 1024.0 / 1024.0) + " MB"
    results['nestedGeneration'] = generationTime

    with open(".test_WebElements_Benchmark.results", 'w') as resultFile:
        resultFile.write(pickle.dumps(results))
