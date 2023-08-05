#ifndef __NOD_DISC_WII__
#define __NOD_DISC_WII__

#include "DiscBase.hpp"

namespace nod
{
class DiscBuilderWii;

class DiscWii : public DiscBase
{
public:
    DiscWii(std::unique_ptr<IDiscIO>&& dio, bool& err);
    DiscBuilderWii makeMergeBuilder(const SystemChar* outPath, bool dualLayer, FProgress progressCB);
    bool extractDiscHeaderFiles(const SystemString& path, const ExtractionContext& ctx) const;
};

class DiscBuilderWii : public DiscBuilderBase
{
    bool m_dualLayer;
public:
    DiscBuilderWii(const SystemChar* outPath, bool dualLayer, FProgress progressCB);
    EBuildResult buildFromDirectory(const SystemChar* dirIn);
    static uint64_t CalculateTotalSizeRequired(const SystemChar* dirIn, bool& dualLayer);
};

class DiscMergerWii
{
    DiscWii& m_sourceDisc;
    DiscBuilderWii m_builder;
public:
    DiscMergerWii(const SystemChar* outPath, DiscWii& sourceDisc,
                  bool dualLayer, FProgress progressCB);
    EBuildResult mergeFromDirectory(const SystemChar* dirIn);
    static uint64_t CalculateTotalSizeRequired(DiscWii& sourceDisc, const SystemChar* dirIn,
                                               bool& dualLayer);
};

}

#endif // __NOD_DISC_WII__
